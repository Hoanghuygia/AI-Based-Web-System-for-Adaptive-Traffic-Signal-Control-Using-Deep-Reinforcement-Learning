from gym import spaces
from typing import List, Dict
from traffic_phase import TrafficPhase
import numpy as np

class TrafficActionSpace:
    """Defines the action space for a traffic control agent."""

    def __init__(self, junction_id: str, phase_mapping: Dict[int, TrafficPhase], 
                 min_phase_duration: int = 15, max_phase_duration: int = 120):
        """
        Args:
            junction_id: ID of the junction to identify its phase mapping
            phase_mapping: Mapping from SUMO phases to internal TrafficPhase
            min_phase_duration: Minimum duration a phase must run before switching
            max_phase_duration: Maximum allowed duration of a single phase
        """
        self.junction_id = junction_id
        self.phase_mapping = phase_mapping
        self.min_phase_duration = min_phase_duration
        self.max_phase_duration = max_phase_duration

        self.available_phases = list(set(phase_mapping.values()) - {None})

        self.actions = {
            0: "KEEP_CURRENT_PHASE",
            1: "EXTEND_CURRENT_PHASE",
            2: "EARLY_TERMINATION"
        }

        for i, phase in enumerate(self.available_phases, start=3):
            self.actions[i] = f"SWITCH_TO_{phase.name}"

        self.num_actions = len(self.actions)
        self.action_space = spaces.Discrete(self.num_actions)

    def is_valid_action(self, action: int, current_phase: TrafficPhase, 
                        phase_duration: int) -> bool:
        """
        Checks whether an action is valid based on the current phase and its duration.
        """
        if current_phase not in self.available_phases:
            return False
        if action not in self.actions:
            return False

        action_name = self.actions[action]

        if action_name == "KEEP_CURRENT_PHASE":
            return phase_duration < self.max_phase_duration
        elif action_name == "EXTEND_CURRENT_PHASE":
            return phase_duration < self.max_phase_duration
        elif action_name == "EARLY_TERMINATION":
            return phase_duration >= self.min_phase_duration
        elif action_name.startswith("SWITCH_TO_"):
            target_phase_name = action_name.replace("SWITCH_TO_", "")
            try:
                target_phase = TrafficPhase[target_phase_name]
                return (current_phase != target_phase and 
                        phase_duration >= self.min_phase_duration)
            except KeyError:
                return False
        return False

    def get_valid_actions(self, current_phase: TrafficPhase, 
                          phase_duration: int) -> List[int]:
        """
        Returns a list of all currently valid actions.
        """
        return [action for action in self.actions 
                if self.is_valid_action(action, current_phase, phase_duration)]
