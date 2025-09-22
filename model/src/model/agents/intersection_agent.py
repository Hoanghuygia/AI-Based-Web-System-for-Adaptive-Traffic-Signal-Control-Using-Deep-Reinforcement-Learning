import numpy as np
import gym
from gym import spaces
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid
from collections import deque
import threading
import time

class MessageType(Enum):
    """Định nghĩa các loại message giữa agents"""
    STATE_BROADCAST = "state_broadcast"
    ACTION_REQUEST = "action_request"
    ACTION_RESPONSE = "action_response"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    EMERGENCY_SIGNAL = "emergency_signal"

@dataclass
class AgentMessage:
    """Cấu trúc message giữa các agents"""
    sender_id: str
    receiver_id: str  # "ALL" for broadcast
    message_type: MessageType
    timestamp: float
    content: Dict[str, Any]
    priority: int = 1  # 1=low, 5=high
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class IntersectionAgent:
    """Agent điều khiển một intersection"""
    
    def __init__(self, agent_id: str, intersection_id: str, 
                 position: Tuple[float, float], 
                 neighboring_agents: List[str],
                 state_space_config: Dict[str, Any],
                 action_space_config: Dict[str, Any]):
        
        self.agent_id = agent_id
        self.intersection_id = intersection_id
        self.position = position
        self.neighboring_agents = neighboring_agents
        
        # Khởi tạo observation và action spaces
        self.local_observation_space = self._create_local_observation_space(state_space_config)
        self.global_observation_space = self._create_global_observation_space(state_space_config)
        self.action_space = spaces.Discrete(action_space_config.get('num_actions', 5))
        
        # Communication components
        self.message_queue = deque(maxlen=100)
        self.outgoing_messages = deque(maxlen=50)
        self.neighbor_states = {neighbor: None for neighbor in neighboring_agents}
        self.last_communication_time = {}
        
        # Agent state
        self.current_state = None
        self.current_action = None
        self.last_action_time = time.time()
        self.coordination_requests = {}
        
        # Performance metrics
        self.performance_history = deque(maxlen=1000)
        self.coordination_success_rate = 0.0
        
    def _create_local_observation_space(self, config: Dict[str, Any]) -> spaces.Box:
        """Tạo local observation space cho agent"""
        num_lanes = config.get('num_lanes', 4)
        
        # Local state components
        local_state_size = (
            num_lanes * 3 +  # queue_lengths, densities, waiting_times
            3 +              # current_phase, phase_duration, time_since_change
            2                # position coordinates
        )
        
        low = np.zeros(local_state_size)
        high = np.ones(local_state_size)
        
        # Adjust bounds for position
        high[-2:] = [1000.0, 1000.0]  # Max position coordinates
        
        return spaces.Box(low=low, high=high, dtype=np.float32)
    
    def _create_global_observation_space(self, config: Dict[str, Any]) -> spaces.Box:
        """Tạo global observation space bao gồm thông tin từ neighbors"""
        local_size = self.local_observation_space.shape[0]
        max_neighbors = config.get('max_neighbors', 8)
        
        # Global state = local state + neighbor states + communication features
        global_state_size = (
            local_size +                    # Local state
            max_neighbors * local_size +    # Neighbor states
            max_neighbors +                 # Communication delays
            len(MessageType) +              # Message type counts
            3                               # Global coordination features
        )
        
        low = np.zeros(global_state_size)
        high = np.ones(global_state_size)
        
        # Adjust bounds
        high[local_size:local_size + max_neighbors * local_size] = 1000.0
        high[-max_neighbors-len(MessageType)-3:-len(MessageType)-3] = 100.0  # Communication delays
        
        return spaces.Box(low=low, high=high, dtype=np.float32)
    
    def get_local_observation(self, raw_state: Dict[str, Any]) -> np.ndarray:
        """Tạo local observation từ raw state"""
        # Normalize state components
        queue_lengths = np.array(raw_state['queue_lengths']) / 50.0
        densities = np.array(raw_state['densities'])
        waiting_times = np.array(raw_state['waiting_times']) / 300.0
        
        current_phase = raw_state['current_phase'] / 4.0
        phase_duration = min(raw_state['phase_duration'], 120.0) / 120.0
        time_since_change = min(raw_state['time_since_last_change'], 300.0) / 300.0
        
        # Add position information
        pos_x, pos_y = self.position
        normalized_pos = [pos_x / 1000.0, pos_y / 1000.0]
        
        # Combine all features
        local_obs = np.concatenate([
            queue_lengths,
            densities,
            waiting_times,
            [current_phase, phase_duration, time_since_change],
            normalized_pos
        ]).astype(np.float32)
        
        return local_obs
    
    def get_global_observation(self, raw_state: Dict[str, Any]) -> np.ndarray:
        """Tạo global observation bao gồm neighbor information"""
        local_obs = self.get_local_observation(raw_state)
        
        # Collect neighbor observations
        neighbor_obs = []
        communication_delays = []
        
        max_neighbors = 8  # Config parameter
        current_time = time.time()
        
        for i, neighbor_id in enumerate(self.neighboring_agents[:max_neighbors]):
            if neighbor_id in self.neighbor_states and self.neighbor_states[neighbor_id] is not None:
                neighbor_obs.extend(self.neighbor_states[neighbor_id])
                # Communication delay
                last_comm_time = self.last_communication_time.get(neighbor_id, current_time)
                delay = min(current_time - last_comm_time, 100.0) / 100.0
                communication_delays.append(delay)
            else:
                # Unknown neighbor state
                neighbor_obs.extend(np.zeros(local_obs.shape[0]))
                communication_delays.append(1.0)  # Max delay
        
        # Pad if we have fewer neighbors than max
        while len(communication_delays) < max_neighbors:
            neighbor_obs.extend(np.zeros(local_obs.shape[0]))
            communication_delays.append(1.0)
        
        # Message type statistics
        message_counts = [0] * len(MessageType)
        for msg in list(self.message_queue)[-10:]:  # Last 10 messages
            msg_type_idx = list(MessageType).index(msg.message_type)
            message_counts[msg_type_idx] += 1
        
        # Normalize message counts
        message_counts = np.array(message_counts) / 10.0
        
        # Global coordination features
        coordination_features = [
            self.coordination_success_rate,
            len(self.coordination_requests) / 10.0,  # Normalize
            min(len(self.message_queue), 100) / 100.0
        ]
        
        # Combine all features
        global_obs = np.concatenate([
            local_obs,
            neighbor_obs,
            communication_delays,
            message_counts,
            coordination_features
        ]).astype(np.float32)
        
        return global_obs
    
    def send_message(self, receiver_id: str, message_type: MessageType, 
                    content: Dict[str, Any], priority: int = 1):
        """Gửi message đến agent khác"""
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            timestamp=time.time(),
            content=content,
            priority=priority
        )
        self.outgoing_messages.append(message)
    
    def receive_message(self, message: AgentMessage):
        """Nhận message từ agent khác"""
        self.message_queue.append(message)
        self.last_communication_time[message.sender_id] = message.timestamp
        
        # Process message based on type
        self._process_message(message)
    
    def _process_message(self, message: AgentMessage):
        """Xử lý message nhận được"""
        if message.message_type == MessageType.STATE_BROADCAST:
            # Update neighbor state
            self.neighbor_states[message.sender_id] = message.content.get('state')
            
        elif message.message_type == MessageType.COORDINATION_REQUEST:
            # Handle coordination request
            self._handle_coordination_request(message)
            
        elif message.message_type == MessageType.EMERGENCY_SIGNAL:
            # Handle emergency situation
            self._handle_emergency_signal(message)
            
        elif message.message_type == MessageType.ACTION_REQUEST:
            # Provide action recommendation
            self._handle_action_request(message)
    
    def _handle_coordination_request(self, message: AgentMessage):
        """Xử lý yêu cầu coordination từ neighbor"""
        request_id = message.content.get('request_id')
        requested_action = message.content.get('requested_action')
        
        # Simple coordination logic
        can_coordinate = self._can_coordinate_with_action(requested_action)
        
        response_content = {
            'request_id': request_id,
            'can_coordinate': can_coordinate,
            'my_planned_action': self.current_action,
            'confidence': 0.8 if can_coordinate else 0.2
        }
        
        self.send_message(
            message.sender_id,
            MessageType.COORDINATION_RESPONSE,
            response_content,
            priority=3
        )
    
    def _can_coordinate_with_action(self, neighbor_action: int) -> bool:
        """Kiểm tra có thể coordinate với action của neighbor không"""
        # Implement coordination logic based on traffic patterns
        # This is a simplified version
        if self.current_action is None:
            return True
        
        # Avoid conflicting actions (e.g., both switching at same time)
        conflicting_actions = [(1, 2), (2, 1)]  # NS_GREEN vs EW_GREEN
        current_pair = (self.current_action, neighbor_action)
        
        return current_pair not in conflicting_actions
    
    def _handle_emergency_signal(self, message: AgentMessage):
        """Xử lý tín hiệu khẩn cấp"""
        emergency_type = message.content.get('emergency_type')
        emergency_location = message.content.get('location')
        
        # Adjust behavior based on emergency
        if emergency_type == 'ambulance':
            # Prioritize clearing path for emergency vehicles
            pass
        elif emergency_type == 'accident':
            # Reduce traffic flow toward accident location
            pass
    
    def _handle_action_request(self, message: AgentMessage):
        """Xử lý yêu cầu đề xuất action"""
        neighbor_state = message.content.get('state')
        
        # Simple action recommendation based on neighbor's state
        recommended_action = self._recommend_action_for_neighbor(neighbor_state)
        
        response_content = {
            'recommended_action': recommended_action,
            'confidence': 0.6
        }
        
        self.send_message(
            message.sender_id,
            MessageType.ACTION_RESPONSE,
            response_content
        )
    
    def _recommend_action_for_neighbor(self, neighbor_state: Dict[str, Any]) -> int:
        """Đề xuất action cho neighbor dựa trên state của họ"""
        # Simple heuristic-based recommendation
        total_queue = sum(neighbor_state.get('queue_lengths', [0, 0, 0, 0]))
        avg_waiting = np.mean(neighbor_state.get('waiting_times', [0, 0, 0, 0]))
        
        if total_queue > 30 or avg_waiting > 60:
            return 3  # EXTEND_CURRENT_PHASE
        elif total_queue < 10 and avg_waiting < 20:
            return 4  # EARLY_TERMINATION
        else:
            return 0  # KEEP_CURRENT_PHASE
    
    def broadcast_state(self, current_state: Dict[str, Any]):
        """Broadcast state đến tất cả neighbors"""
        self.current_state = current_state
        
        broadcast_content = {
            'state': self.get_local_observation(current_state).tolist(),
            'timestamp': time.time(),
            'performance': self.get_recent_performance()
        }
        
        self.send_message(
            "ALL",
            MessageType.STATE_BROADCAST,
            broadcast_content,
            priority=2
        )
    
    def get_recent_performance(self) -> Dict[str, float]:
        """Lấy performance metrics gần đây"""
        if len(self.performance_history) == 0:
            return {'avg_reward': 0.0, 'success_rate': 0.0}
        
        recent_rewards = list(self.performance_history)[-100:]
        return {
            'avg_reward': np.mean(recent_rewards),
            'success_rate': self.coordination_success_rate
        }
    
    def update_performance(self, reward: float, coordination_success: bool):
        """Cập nhật performance metrics"""
        self.performance_history.append(reward)
        
        # Update coordination success rate with exponential moving average
        alpha = 0.1
        success_value = 1.0 if coordination_success else 0.0
        self.coordination_success_rate = (
            alpha * success_value + (1 - alpha) * self.coordination_success_rate
        )