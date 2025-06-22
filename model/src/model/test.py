import numpy as np
import gym
from gym import spaces
from typing import Dict, List, Tuple, Any
from enum import Enum

class TrafficPhase(Enum):
    """Định nghĩa các pha đèn giao thông"""
    NORTH_SOUTH_GREEN = 0
    NORTH_SOUTH_YELLOW = 1
    EAST_WEST_GREEN = 2
    EAST_WEST_YELLOW = 3
    ALL_RED = 4

class TrafficStateSpace:
    """Định nghĩa không gian trạng thái cho traffic control agent"""
    
    def __init__(self, max_queue_length: int = 50, max_density: float = 1.0, 
                 max_waiting_time: float = 300.0, num_lanes: int = 4):
        self.max_queue_length = max_queue_length
        self.max_density = max_density
        self.max_waiting_time = max_waiting_time
        self.num_lanes = num_lanes
        
        # Định nghĩa các thành phần của state
        self.state_components = {
            'queue_lengths': num_lanes,      # the reason why it assigned to num-lanes is because each lane has its own queue length
            'densities': num_lanes,          # Mật độ xe mỗi lane
            'waiting_times': num_lanes,      # Thời gian chờ trung bình mỗi lane
            'current_phase': 1,              # Pha đèn hiện tại
            'phase_duration': 1,             # Thời gian pha đèn đã chạy
            'time_since_last_change': 1      # Thời gian từ lần thay đổi cuối
        }
        
        # Tổng số features
        self.state_size = sum(self.state_components.values())
        
        # Định nghĩa observation space
        self.observation_space = self._create_observation_space()
    
    def _create_observation_space(self) -> spaces.Box:
        """Tạo observation space cho gym environment"""
        # Định nghĩa bounds cho từng thành phần
        low = np.concatenate([
            np.zeros(self.num_lanes),           # queue_lengths >= 0
            np.zeros(self.num_lanes),           # densities >= 0
            np.zeros(self.num_lanes),           # waiting_times >= 0
            np.array([0]),                      # current_phase >= 0
            np.array([0]),                      # phase_duration >= 0
            np.array([0])                       # time_since_last_change >= 0
        ])
        
        high = np.concatenate([
            np.full(self.num_lanes, self.max_queue_length),
            np.full(self.num_lanes, self.max_density),
            np.full(self.num_lanes, self.max_waiting_time),
            np.array([len(TrafficPhase) - 1]),
            np.array([300.0]),                  # max phase duration
            np.array([300.0])                   # max time since change
        ])
        
        return spaces.Box(low=low, high=high, dtype=np.float32)
    
    def normalize_state(self, raw_state: Dict[str, Any]) -> np.ndarray:
        """Chuẩn hóa raw state thành normalized vector"""
        # Chuẩn hóa queue lengths
        queue_lengths = np.array(raw_state['queue_lengths']) / self.max_queue_length
        queue_lengths = np.clip(queue_lengths, 0, 1)
        
        # Chuẩn hóa densities
        densities = np.array(raw_state['densities']) / self.max_density
        densities = np.clip(densities, 0, 1)
        
        # Chuẩn hóa waiting times
        waiting_times = np.array(raw_state['waiting_times']) / self.max_waiting_time
        waiting_times = np.clip(waiting_times, 0, 1)
        
        # Chuẩn hóa current phase
        current_phase = raw_state['current_phase'] / (len(TrafficPhase) - 1)
        
        # Chuẩn hóa phase duration
        phase_duration = min(raw_state['phase_duration'], 300.0) / 300.0
        
        # Chuẩn hóa time since last change
        time_since_change = min(raw_state['time_since_last_change'], 300.0) / 300.0
        
        # Kết hợp tất cả thành vector
        normalized_state = np.concatenate([
            queue_lengths,
            densities,
            waiting_times,
            [current_phase],
            [phase_duration],
            [time_since_change]
        ]).astype(np.float32)
        
        return normalized_state

class TrafficActionSpace:
    """Định nghĩa không gian hành động cho traffic control agent"""
    
    def __init__(self, min_phase_duration: int = 10, max_phase_duration: int = 120):
        self.min_phase_duration = min_phase_duration
        self.max_phase_duration = max_phase_duration
        
        # Định nghĩa các hành động có thể
        self.actions = {
            0: "KEEP_CURRENT_PHASE",     # Giữ nguyên pha hiện tại
            1: "SWITCH_TO_NS_GREEN",     # Chuyển sang pha North-South xanh
            2: "SWITCH_TO_EW_GREEN",     # Chuyển sang pha East-West xanh
            3: "EXTEND_CURRENT_PHASE",   # Kéo dài pha hiện tại
            4: "EARLY_TERMINATION"       # Kết thúc sớm pha hiện tại
        }
        
        self.num_actions = len(self.actions)
        
        # Tạo action space
        self.action_space = spaces.Discrete(self.num_actions)
    
    def is_valid_action(self, action: int, current_phase: TrafficPhase, 
                       phase_duration: int) -> bool:
        """Kiểm tra tính hợp lệ của action"""
        if action == 0:  # KEEP_CURRENT_PHASE
            return phase_duration < self.max_phase_duration
        
        elif action == 1:  # SWITCH_TO_NS_GREEN
            return (current_phase != TrafficPhase.NORTH_SOUTH_GREEN and 
                   phase_duration >= self.min_phase_duration)
        
        elif action == 2:  # SWITCH_TO_EW_GREEN
            return (current_phase != TrafficPhase.EAST_WEST_GREEN and 
                   phase_duration >= self.min_phase_duration)
        
        elif action == 3:  # EXTEND_CURRENT_PHASE
            return phase_duration < self.max_phase_duration
        
        elif action == 4:  # EARLY_TERMINATION
            return phase_duration >= self.min_phase_duration
        
        return False
    
    def get_valid_actions(self, current_phase: TrafficPhase, 
                         phase_duration: int) -> List[int]:
        """Lấy danh sách các action hợp lệ"""
        valid_actions = []
        for action in range(self.num_actions):
            if self.is_valid_action(action, current_phase, phase_duration):
                valid_actions.append(action)
        return valid_actions

class TrafficRewardFunction:
    """Định nghĩa hàm reward cho traffic control"""
    
    def __init__(self, queue_weight: float = 0.4, waiting_weight: float = 0.4, 
                 throughput_weight: float = 0.2, penalty_weight: float = 0.1):
        self.queue_weight = queue_weight
        self.waiting_weight = waiting_weight
        self.throughput_weight = throughput_weight
        self.penalty_weight = penalty_weight
    
    def calculate_reward(self, prev_state: Dict[str, Any], 
                        current_state: Dict[str, Any], 
                        action: int, throughput: int) -> float:
        """Tính toán reward dựa trên state transition"""
        
        # 1. Queue length reward (càng ít xe xếp hàng càng tốt)
        prev_total_queue = sum(prev_state['queue_lengths'])
        curr_total_queue = sum(current_state['queue_lengths'])
        queue_reward = (prev_total_queue - curr_total_queue) * self.queue_weight
        
        # 2. Waiting time reward (càng ít thời gian chờ càng tốt)
        prev_avg_waiting = np.mean(prev_state['waiting_times'])
        curr_avg_waiting = np.mean(current_state['waiting_times'])
        waiting_reward = (prev_avg_waiting - curr_avg_waiting) * self.waiting_weight
        
        # 3. Throughput reward (càng nhiều xe qua giao lộ càng tốt)
        throughput_reward = throughput * self.throughput_weight
        
        # 4. Penalty cho việc thay đổi pha quá thường xuyên
        phase_change_penalty = 0
        if (prev_state['current_phase'] != current_state['current_phase'] and 
            prev_state['phase_duration'] < 15):  # Thay đổi quá sớm
            phase_change_penalty = -5 * self.penalty_weight
        
        # Tổng reward
        total_reward = (queue_reward + waiting_reward + 
                       throughput_reward + phase_change_penalty)
        
        return float(total_reward)
    
    def calculate_global_reward(self, all_agents_rewards: List[float]) -> float:
        """Tính toán global reward cho multi-agent system"""
        # Có thể sử dụng trung bình hoặc tổng của các rewards
        return np.mean(all_agents_rewards)

class TrafficControlSpaceManager:
    """Manager class để quản lý tất cả các không gian cho traffic control"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Khởi tạo các component
        self.state_space = TrafficStateSpace(
            max_queue_length=config.get('max_queue_length', 50),
            max_density=config.get('max_density', 1.0),
            max_waiting_time=config.get('max_waiting_time', 300.0),
            num_lanes=config.get('num_lanes', 4)
        )
        
        self.action_space = TrafficActionSpace(
            min_phase_duration=config.get('min_phase_duration', 10),
            max_phase_duration=config.get('max_phase_duration', 120)
        )
        
        self.reward_function = TrafficRewardFunction(
            queue_weight=config.get('queue_weight', 0.4),
            waiting_weight=config.get('waiting_weight', 0.4),
            throughput_weight=config.get('throughput_weight', 0.2),
            penalty_weight=config.get('penalty_weight', 0.1)
        )
    
    def get_observation_space(self) -> spaces.Box:
        """Trả về observation space"""
        return self.state_space.observation_space
    
    def get_action_space(self) -> spaces.Discrete:
        """Trả về action space"""
        return self.action_space.action_space
    
    def process_state(self, raw_state: Dict[str, Any]) -> np.ndarray:
        """Xử lý raw state thành normalized state"""
        return self.state_space.normalize_state(raw_state)
    
    def validate_action(self, action: int, current_phase: TrafficPhase, 
                       phase_duration: int) -> bool:
        """Kiểm tra tính hợp lệ của action"""
        return self.action_space.is_valid_action(action, current_phase, phase_duration)
    
    def calculate_reward(self, prev_state: Dict[str, Any], 
                        current_state: Dict[str, Any], 
                        action: int, throughput: int) -> float:
        """Tính reward"""
        return self.reward_function.calculate_reward(
            prev_state, current_state, action, throughput)

# Example usage
# if __name__ == "__main__":
#     # Cấu hình cho hệ thống
#     config = {
#         'max_queue_length': 50,
#         'max_density': 1.0,
#         'max_waiting_time': 300.0,
#         'num_lanes': 4,
#         'min_phase_duration': 10,
#         'max_phase_duration': 120,
#         'queue_weight': 0.4,
#         'waiting_weight': 0.4,
#         'throughput_weight': 0.2,
#         'penalty_weight': 0.1
#     }
    
#     # Khởi tạo manager
#     manager = TrafficControlSpaceManager(config)
    
#     # Test với dữ liệu mẫu
#     raw_state = {
#         'queue_lengths': [10, 15, 8, 12],
#         'densities': [0.3, 0.5, 0.2, 0.4],
#         'waiting_times': [30, 45, 20, 35],
#         'current_phase': 0,
#         'phase_duration': 25,
#         'time_since_last_change': 25
#     }
    
#     # Xử lý state
#     normalized_state = manager.process_state(raw_state)
#     print(f"Normalized state shape: {normalized_state.shape}")
#     print(f"Normalized state: {normalized_state}")
    
#     # Kiểm tra action space
#     print(f"Action space: {manager.get_action_space()}")
#     print(f"Observation space: {manager.get_observation_space()}")
    
#     # Test valid actions
#     valid_actions = manager.action_space.get_valid_actions(
#         TrafficPhase.NORTH_SOUTH_GREEN, 25)
#     print(f"Valid actions: {valid_actions}")