import numpy as np
from gym import spaces
from typing import Dict, Any
from traffic_phase import TrafficPhase

class TrafficStateSpace:
    def __init__(self, max_queue_length: int = 50, max_density: float = 1.0, 
                 max_waiting_time: float = 300.0, num_lanes: int = 4, junction_id: str = None, 
                 phase_mapping: Dict[int, TrafficPhase] = None):
        self.max_queue_length = max_queue_length
        self.max_density = max_density
        self.max_waiting_time = max_waiting_time
        self.num_lanes = num_lanes
        self.junction_id = junction_id
        if phase_mapping is None:
            self.phase_mapping = {phase.value: phase for phase in TrafficPhase}
        else:
            self.phase_mapping = phase_mapping
        
        self.state_components = {
            'queue_lengths': num_lanes,
            'densities': num_lanes,
            'waiting_times': num_lanes,
            'current_phase': 1,
            'phase_duration': 1,
            'time_since_last_change': 1
        }

        self.state_size = sum(self.state_components.values())
        self.observation_space = self._create_observation_space()
    
    def _create_observation_space(self) -> spaces.Box:
        low = np.concatenate([
            np.zeros(self.num_lanes),
            np.zeros(self.num_lanes),
            np.zeros(self.num_lanes),
            np.array([0]),
            np.array([0]),
            np.array([0])
        ])
        
        high = np.concatenate([
            np.full(self.num_lanes, self.max_queue_length),
            np.full(self.num_lanes, self.max_density),
            np.full(self.num_lanes, self.max_waiting_time),
            np.array([len(TrafficPhase) - 1]),
            np.array([300.0]),
            np.array([300.0])
        ])
        
        return spaces.Box(low=low, high=high, dtype=np.float32)
    
    def normalize_state(self, raw_state: Dict[str, Any]) -> np.ndarray:
        queue_lengths = np.array(raw_state['queue_lengths']) / self.max_queue_length
        queue_lengths = np.clip(queue_lengths, 0, 1)
        
        densities = np.array(raw_state['densities']) / self.max_density
        densities = np.clip(densities, 0, 1)
        
        waiting_times = np.array(raw_state['waiting_times']) / self.max_waiting_time
        waiting_times = np.clip(waiting_times, 0, 1)
        
        sumo_phase = raw_state['current_phase']
        traffic_phase = self.phase_mapping.get(sumo_phase, None)
        if traffic_phase is None:
            raise ValueError(f"Invalid SUMO phase {sumo_phase} for junction {self.junction_id}")
        
        available_phases = list(set(self.phase_mapping.values()) - {None})
        current_phase_idx = available_phases.index(traffic_phase) if traffic_phase in available_phases else 0
        current_phase = current_phase_idx / (len(available_phases) - 1) if len(available_phases) > 1 else 0.0
        
        phase_duration = min(raw_state['phase_duration'], 300.0) / 300.0
        time_since_change = min(raw_state['time_since_last_change'], 300.0) / 300.0
        
        normalized_state = np.concatenate([
            queue_lengths,
            densities,
            waiting_times,
            [current_phase],
            [phase_duration],
            [time_since_change]
        ]).astype(np.float32)
        
        return normalized_state
