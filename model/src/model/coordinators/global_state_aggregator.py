import torch
from typing import Dict
from collections import deque

class GlobalStateAggregator:
    """Aggregate global state information for centralized training"""
    
    def __init__(self, num_agents: int):
        self.num_agents = num_agents
        self.state_history = deque(maxlen=100)
    
    def aggregate_states(self, agent_states: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Aggregate individual agent states into global state"""
        # Sort agents for consistent ordering
        sorted_agents = sorted(agent_states.keys())
        
        # Concatenate states
        global_state = torch.cat([
            agent_states[agent_id] for agent_id in sorted_agents
        ])
        
        # Store in history
        self.state_history.append(global_state.clone())
        
        return global_state
    
    def get_state_statistics(self) -> Dict[str, float]:
        """Get statistics about global states"""
        if not self.state_history:
            return {}
        
        states = torch.stack(list(self.state_history))
        
        return {
            'mean': states.mean().item(),
            'std': states.std().item(),
            'min': states.min().item(),
            'max': states.max().item()
        }