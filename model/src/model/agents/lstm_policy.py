import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from ..configs.network_config import NetworkConfig

class LSTMPolicyNetwork(nn.Module):
    """LSTM-based Policy Network cho mỗi agent"""
    
    def __init__(self, config: NetworkConfig, action_space_size: int):
        super(LSTMPolicyNetwork, self).__init__()
        
        self.config = config
        self.action_space_size = action_space_size
        self.device = config.device
        
        # Input processing layers
        self.input_norm = nn.LayerNorm(config.input_size)
        self.input_fc = nn.Linear(config.input_size, config.hidden_size)
        
        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=config.hidden_size,
            hidden_size=config.hidden_size,
            num_layers=config.num_layers,
            dropout=config.dropout if config.num_layers > 1 else 0,
            batch_first=True
        )
        
        # Policy head (actor)
        self.policy_head = nn.Sequential(
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size, config.hidden_size // 2),
            nn.ReLU(),
            nn.Linear(config.hidden_size // 2, action_space_size)
        )
        
        # Value head (critic)
        self.value_head = nn.Sequential(
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size, config.hidden_size // 2),
            nn.ReLU(),
            nn.Linear(config.hidden_size // 2, 1)
        )
        
        # Attention mechanism for multi-agent coordination
        self.attention = nn.MultiheadAttention(
            embed_dim=config.hidden_size,
            num_heads=8,
            dropout=config.dropout,
            batch_first=True
        )
        
        # Initialize weights
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        """Initialize network weights"""
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.LSTM):
            for name, param in module.named_parameters():
                if 'weight' in name:
                    torch.nn.init.xavier_uniform_(param)
                elif 'bias' in name:
                    torch.nn.init.zeros_(param)
    
    def forward(self, state, hidden_state=None, mask=None):
        """Forward pass through network"""
        batch_size = state.size(0)
        seq_len = state.size(1) if len(state.shape) == 3 else 1
        
        # Handle single step vs sequence
        if len(state.shape) == 2:
            state = state.unsqueeze(1)  # Add sequence dimension
        
        # Input processing
        state = self.input_norm(state)
        processed_input = F.relu(self.input_fc(state))
        
        # LSTM forward pass
        if hidden_state is None:
            lstm_out, hidden_state = self.lstm(processed_input)
        else:
            lstm_out, hidden_state = self.lstm(processed_input, hidden_state)
        
        # Apply attention if we have sequence data
        if seq_len > 1:
            attended_out, attention_weights = self.attention(
                lstm_out, lstm_out, lstm_out, key_padding_mask=mask
            )
            lstm_out = lstm_out + attended_out  # Residual connection
        
        # Get last timestep output
        if seq_len > 1:
            last_output = lstm_out[:, -1, :]
        else:
            last_output = lstm_out.squeeze(1)
        
        # Policy and value outputs
        logits = self.policy_head(last_output)
        value = self.value_head(last_output)
        
        return logits, value, hidden_state
    
    def get_action_and_value(self, state, hidden_state=None, mask=None, 
                           valid_actions=None):
        """Get action distribution and value estimate"""
        logits, value, new_hidden_state = self.forward(state, hidden_state, mask)
        
        # Apply valid action mask if provided
        if valid_actions is not None:
            logits = self._apply_action_mask(logits, valid_actions)
        
        # Create action distribution
        probs = F.softmax(logits, dim=-1)
        dist = Categorical(probs)
        
        # Sample action
        action = dist.sample()
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()
        
        return {
            'action': action,
            'log_prob': log_prob,
            'value': value.squeeze(-1),
            'entropy': entropy,
            'hidden_state': new_hidden_state,
            'action_probs': probs
        }
    
    def _apply_action_mask(self, logits, valid_actions):
        """Apply mask for invalid actions"""
        masked_logits = logits.clone()
        
        # Set invalid actions to large negative value
        for i, valid_acts in enumerate(valid_actions):
            invalid_mask = torch.ones(self.action_space_size, dtype=torch.bool)
            invalid_mask[valid_acts] = False
            masked_logits[i, invalid_mask] = -1e8
        
        return masked_logits
    
    def evaluate_actions(self, states, actions, hidden_states=None, masks=None):
        """Evaluate actions for training"""
        logits, values, _ = self.forward(states, hidden_states, masks)
        
        dist = Categorical(logits=logits)
        log_probs = dist.log_prob(actions)
        entropy = dist.entropy()
        
        return log_probs, values.squeeze(-1), entropy