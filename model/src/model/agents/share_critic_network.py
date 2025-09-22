import torch
import torch.nn as nn

from ..configs.network_config import NetworkConfig

class SharedCriticNetwork(nn.Module):
    """Shared Critic Network cho centralized training"""
    
    def __init__(self, config: NetworkConfig, num_agents: int):
        super(SharedCriticNetwork, self).__init__()
        
        self.num_agents = num_agents
        
        # Global state processing
        global_input_size = config.input_size * num_agents
        
        self.global_norm = nn.LayerNorm(global_input_size)
        self.global_fc = nn.Sequential(
            nn.Linear(global_input_size, config.hidden_size * 2),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size * 2, config.hidden_size)
        )
        
        # LSTM for temporal processing
        self.lstm = nn.LSTM(
            input_size=config.hidden_size,
            hidden_size=config.hidden_size,
            num_layers=config.num_layers,
            dropout=config.dropout if config.num_layers > 1 else 0,
            batch_first=True
        )
        
        # Value head
        self.value_head = nn.Sequential(
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size, config.hidden_size // 2),
            nn.ReLU(),
            nn.Linear(config.hidden_size // 2, num_agents)  # Value for each agent
        )
        
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
    
    def forward(self, global_states, hidden_state=None):
        """Forward pass for global value estimation"""
        batch_size = global_states.size(0)
        
        if len(global_states.shape) == 2:
            global_states = global_states.unsqueeze(1)
        
        # Process global state
        normalized_states = self.global_norm(global_states)
        processed_states = self.global_fc(normalized_states)
        
        # LSTM processing
        if hidden_state is None:
            lstm_out, hidden_state = self.lstm(processed_states)
        else:
            lstm_out, hidden_state = self.lstm(processed_states, hidden_state)
        
        # Get last timestep
        last_output = lstm_out[:, -1, :] if lstm_out.size(1) > 1 else lstm_out.squeeze(1)
        
        # Value estimation
        values = self.value_head(last_output)
        
        return values, hidden_state