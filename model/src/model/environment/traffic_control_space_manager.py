from traffic_phase import TrafficPhase
from traffic_state_space import TrafficStateSpace
from traffic_action_space import TrafficActionSpace
from traffic_reward_function import TrafficRewardFunction

from gym import spaces
from typing import List, Dict, Any
import numpy as np

class TrafficControlSpaceManager:
    """Manager class để quản lý tất cả các không gian cho traffic control"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Khởi tạo các component
        self.state_space = TrafficStateSpace(
            max_queue_length=config.get('max_queue_length', 50),
            max_density=config.get('max_density', 1.0),
            max_waiting_time=config.get('max_waiting_time', 300.0),
            num_lanes=config.get('num_lanes', 4),
            junction_id=config.get('junction_id', None),
            phase_mapping=config.get('phase_mapping', None)
        )
        
        self.action_space = TrafficActionSpace(
            phase_mapping=config.get('phase_mapping', None),
            min_phase_duration=config.get('min_phase_duration', 15),
            max_phase_duration=config.get('max_phase_duration', 120)
        )
        
        self.reward_function = TrafficRewardFunction(
            state_space=self.state_space,
            queue_weight=config.get('queue_weight', 0.4),
            waiting_weight=config.get('waiting_weight', 0.4),
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