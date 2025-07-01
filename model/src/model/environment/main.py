from traffic_control_space_manager import TrafficControlSpaceManager
from traffic_phase import TrafficPhase
# Example usage
if __name__ == "__main__":
    # Cấu hình cho hệ thống
    config = {
        'max_queue_length': 50,
        'max_density': 1.0,
        'max_waiting_time': 300.0,
        'num_lanes': 4,
        'min_phase_duration': 15,
        'max_phase_duration': 120,
        'queue_weight': 0.4,
        'waiting_weight': 0.38,
        'throughput_weight': 0.2,
        'penalty_weight': 0.1,
        'soft_queue_penalty_weight': 0.02,
        'junction_id': 'junction_1',
        'phase_mapping': {
            0: TrafficPhase.NORTH_SOUTH_GREEN,
            1: TrafficPhase.NORTH_SOUTH_YELLOW,
            2: TrafficPhase.EAST_WEST_GREEN,
            3: TrafficPhase.EAST_WEST_YELLOW,
            4: TrafficPhase.ALL_RED,
            5: TrafficPhase.TRANSITION
        }
    }
    
    # Khởi tạo manager
    manager = TrafficControlSpaceManager(config)
    
    # Test với dữ liệu mẫu
    raw_state = {
        'queue_lengths': [10, 15, 8, 12],
        'densities': [0.3, 0.5, 0.2, 0.4],
        'waiting_times': [30, 45, 20, 35],
        'current_phase': 0,
        'phase_duration': 25,
        'time_since_last_change': 25
    }
    
    # Xử lý state
    normalized_state = manager.process_state(raw_state)
    print(f"Normalized state shape: {normalized_state.shape}")
    print(f"Normalized state: {normalized_state}")
    
    # Kiểm tra action space
    print(f"Action space: {manager.get_action_space()}")
    print(f"Observation space: {manager.get_observation_space()}")
    
    # Test valid actions
    valid_actions = manager.action_space.get_valid_actions(
        TrafficPhase.NORTH_SOUTH_GREEN, 25)
    print(f"Valid actions: {valid_actions}")