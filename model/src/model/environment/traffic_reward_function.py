from typing import Dict, List, Any
import numpy as np
from traffic_phase import TrafficPhase

class TrafficRewardFunction:
    """Defines the shaped reward function for traffic signal control."""

    def __init__(self, 
                 state_space,
                 queue_weight: float = 0.4, 
                 waiting_weight: float = 0.38, 
                 penalty_weight: float = 0.1,
                 soft_queue_penalty_weight: float = 0.02):
        """
        Args:
            state_space: TrafficStateSpace instance (for normalization factors)
            queue_weight: Weight for queue length reduction reward
            waiting_weight: Weight for waiting time reduction reward
            penalty_weight: Weight for phase switching penalties
            soft_queue_penalty_weight: Mild penalty for remaining queue
        """
        self.state_space = state_space
        self.queue_weight = queue_weight
        self.waiting_weight = waiting_weight
        self.penalty_weight = penalty_weight
        self.soft_queue_penalty_weight = soft_queue_penalty_weight

    def calculate_reward(self, 
                         prev_state: Dict[str, Any], 
                         current_state: Dict[str, Any]) -> float:
        prev_total_queue = sum(prev_state['queue_lengths'])
        curr_total_queue = sum(current_state['queue_lengths'])
        queue_diff = prev_total_queue - curr_total_queue
        queue_score = queue_diff / (self.state_space.max_queue_length * self.state_space.num_lanes)
        queue_reward = queue_score * self.queue_weight

        prev_avg_wait = np.mean(prev_state['waiting_times'])
        curr_avg_wait = np.mean(current_state['waiting_times'])
        wait_diff = prev_avg_wait - curr_avg_wait
        wait_score = wait_diff / self.state_space.max_waiting_time
        waiting_reward = wait_score * self.waiting_weight

        phase_change_penalty = 0.0
        if prev_state['current_phase'] != current_state['current_phase']:
            duration = prev_state['phase_duration']
            max_phase_duration = self.state_space.max_waiting_time  # dùng chung
            normalized_duration = min(duration / max_phase_duration, 1.0)
            phase_change_penalty = - (1 - normalized_duration) * self.penalty_weight

        residual_queue_penalty = -self.soft_queue_penalty_weight * curr_total_queue

        total_reward = (queue_reward + waiting_reward +
                        phase_change_penalty + residual_queue_penalty)
        return float(total_reward)

    def calculate_global_reward(self, all_agents_rewards: List[float]) -> float:
        """Computes the global reward in multi-agent settings."""
        return np.mean(all_agents_rewards)
