import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from typing import Dict, List, Tuple, Any, Optional
from collections import deque, namedtuple
import threading
import time
from dataclasses import dataclass
import pickle

# Experience tuple for storing trajectories
Experience = namedtuple('Experience', [
    'state', 'action', 'reward', 'next_state', 'done', 
    'hidden_state', 'cell_state', 'log_prob', 'value'
])

@dataclass
class NetworkConfig:
    """Configuration cho neural networks"""
    input_size: int
    hidden_size: int = 128
    num_layers: int = 2
    dropout: float = 0.1
    learning_rate: float = 3e-4
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

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

class ExperienceBuffer:
    """Experience buffer cho multi-agent training"""
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.lock = threading.Lock()
    
    def push(self, experience: Experience):
        """Add experience to buffer"""
        with self.lock:
            self.buffer.append(experience)
    
    def sample(self, batch_size: int) -> List[Experience]:
        """Sample batch of experiences"""
        with self.lock:
            if len(self.buffer) < batch_size:
                return list(self.buffer)
            
            indices = np.random.choice(len(self.buffer), batch_size, replace=False)
            return [self.buffer[i] for i in indices]
    
    def get_all(self) -> List[Experience]:
        """Get all experiences"""
        with self.lock:
            return list(self.buffer)
    
    def clear(self):
        """Clear buffer"""
        with self.lock:
            self.buffer.clear()
    
    def __len__(self):
        return len(self.buffer)

class MultiAgentCoordinatorAdvanced:
    """Advanced Multi-Agent Coordinator với centralized training"""
    
    def __init__(self, 
                 agent_configs: Dict[str, NetworkConfig],
                 action_space_sizes: Dict[str, int],
                 coordination_config: Dict[str, Any]):
        
        self.agent_configs = agent_configs
        self.action_space_sizes = action_space_sizes
        self.coordination_config = coordination_config
        self.device = list(agent_configs.values())[0].device
        
        # Initialize networks
        self.policy_networks = {}
        self.optimizers = {}
        
        for agent_id, config in agent_configs.items():
            self.policy_networks[agent_id] = LSTMPolicyNetwork(
                config, action_space_sizes[agent_id]
            ).to(self.device)
            
            self.optimizers[agent_id] = torch.optim.Adam(
                self.policy_networks[agent_id].parameters(),
                lr=config.learning_rate
            )
        
        # Shared critic for centralized training
        num_agents = len(agent_configs)
        shared_config = list(agent_configs.values())[0]
        
        self.shared_critic = SharedCriticNetwork(
            shared_config, num_agents
        ).to(self.device)
        
        self.critic_optimizer = torch.optim.Adam(
            self.shared_critic.parameters(),
            lr=shared_config.learning_rate
        )
        
        # Experience buffer
        self.experience_buffer = ExperienceBuffer(
            coordination_config.get('buffer_size', 10000)
        )
        
        # Hidden states for LSTM
        self.agent_hidden_states = {}
        self.critic_hidden_state = None
        
        # Training statistics
        self.training_stats = {
            'policy_losses': deque(maxlen=1000),
            'value_losses': deque(maxlen=1000),
            'entropy_losses': deque(maxlen=1000),
            'coordination_rewards': deque(maxlen=1000)
        }
        
        # Coordination mechanisms
        self.coordination_matrix = self._initialize_coordination_matrix()
        self.global_state_aggregator = GlobalStateAggregator(num_agents)
        
    def _initialize_coordination_matrix(self) -> torch.Tensor:
        """Initialize coordination matrix for agent interactions"""
        num_agents = len(self.agent_configs)
        # Initialize with small random values
        matrix = torch.randn(num_agents, num_agents) * 0.1
        # Zero diagonal (agent doesn't coordinate with itself)
        matrix.fill_diagonal_(0)
        return matrix.to(self.device)
    
    def get_actions(self, observations: Dict[str, torch.Tensor], 
                   valid_actions: Optional[Dict[str, List[int]]] = None,
                   training: bool = True) -> Dict[str, Dict[str, Any]]:
        """Get actions from all agents"""
        actions_info = {}
        
        # Get individual agent actions
        for agent_id, obs in observations.items():
            if agent_id not in self.policy_networks:
                continue
            
            # Get or initialize hidden state
            hidden_state = self.agent_hidden_states.get(agent_id, None)
            
            # Get valid actions for this agent
            agent_valid_actions = valid_actions.get(agent_id) if valid_actions else None
            
            with torch.no_grad() if not training else torch.enable_grad():
                action_info = self.policy_networks[agent_id].get_action_and_value(
                    obs.unsqueeze(0).to(self.device),
                    hidden_state,
                    valid_actions=agent_valid_actions
                )
            
            # Update hidden state
            self.agent_hidden_states[agent_id] = action_info['hidden_state']
            
            actions_info[agent_id] = action_info
        
        # Apply coordination if enabled
        if self.coordination_config.get('enable_coordination', True):
            actions_info = self._apply_coordination(actions_info, observations)
        
        return actions_info
    
    def _apply_coordination(self, actions_info: Dict[str, Dict[str, Any]], 
                          observations: Dict[str, torch.Tensor]) -> Dict[str, Dict[str, Any]]:
        """Apply coordination mechanism to actions"""
        agent_ids = list(actions_info.keys())
        
        if len(agent_ids) < 2:
            return actions_info
        
        # Get action probabilities
        action_probs = torch.stack([
            actions_info[agent_id]['action_probs'] 
            for agent_id in agent_ids
        ])  # [num_agents, num_actions]
        
        # Apply coordination matrix
        coordinated_probs = torch.matmul(
            self.coordination_matrix[:len(agent_ids), :len(agent_ids)], 
            action_probs
        )
        
        # Normalize probabilities
        coordinated_probs = F.softmax(coordinated_probs, dim=-1)
        
        # Update actions based on coordinated probabilities
        for i, agent_id in enumerate(agent_ids):
            new_dist = Categorical(coordinated_probs[i])
            new_action = new_dist.sample()
            
            actions_info[agent_id]['action'] = new_action
            actions_info[agent_id]['log_prob'] = new_dist.log_prob(new_action)
            actions_info[agent_id]['coordinated'] = True
        
        return actions_info
    
    def store_experience(self, agent_id: str, experience: Experience):
        """Store experience in buffer"""
        self.experience_buffer.push(experience)
    
    def train_step(self, batch_size: int = 32) -> Dict[str, float]:
        """Perform one training step"""
        if len(self.experience_buffer) < batch_size:
            return {}
        
        # Sample experiences
        experiences = self.experience_buffer.sample(batch_size)
        
        # Prepare batch data
        batch_data = self._prepare_batch_data(experiences)
        
        # Train policy networks
        policy_losses = self._train_policies(batch_data)
        
        # Train shared critic
        value_loss = self._train_shared_critic(batch_data)
        
        # Update coordination matrix
        self._update_coordination_matrix(batch_data)
        
        # Compile training statistics
        training_info = {
            'policy_loss': np.mean(list(policy_losses.values())),
            'value_loss': value_loss,
            'buffer_size': len(self.experience_buffer)
        }
        
        # Update statistics
        self.training_stats['policy_losses'].append(training_info['policy_loss'])
        self.training_stats['value_losses'].append(training_info['value_loss'])
        
        return training_info
    
    def _prepare_batch_data(self, experiences: List[Experience]) -> Dict[str, torch.Tensor]:
        """Prepare batch data for training"""
        # Group experiences by agent
        agent_experiences = {}
        
        for exp in experiences:
            # Assuming experience contains agent_id info
            # This would need to be added to Experience namedtuple
            agent_id = getattr(exp, 'agent_id', 'default_agent')
            
            if agent_id not in agent_experiences:
                agent_experiences[agent_id] = []
            agent_experiences[agent_id].append(exp)
        
        # Convert to tensors
        batch_data = {}
        for agent_id, agent_exps in agent_experiences.items():
            states = torch.stack([torch.tensor(exp.state) for exp in agent_exps])
            actions = torch.stack([torch.tensor(exp.action) for exp in agent_exps])
            rewards = torch.stack([torch.tensor(exp.reward) for exp in agent_exps])
            values = torch.stack([torch.tensor(exp.value) for exp in agent_exps])
            log_probs = torch.stack([torch.tensor(exp.log_prob) for exp in agent_exps])
            
            batch_data[agent_id] = {
                'states': states.to(self.device),
                'actions': actions.to(self.device),
                'rewards': rewards.to(self.device),
                'values': values.to(self.device),
                'log_probs': log_probs.to(self.device)
            }
        
        return batch_data
    
    def _train_policies(self, batch_data: Dict[str, Dict[str, torch.Tensor]]) -> Dict[str, float]:
        """Train individual policy networks"""
        policy_losses = {}
        
        for agent_id, data in batch_data.items():
            if agent_id not in self.policy_networks:
                continue
            
            network = self.policy_networks[agent_id]
            optimizer = self.optimizers[agent_id]
            
            # Calculate advantages (simplified)
            advantages = data['rewards'] - data['values']
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
            
            # Policy loss (PPO-style)
            log_probs, values, entropy = network.evaluate_actions(
                data['states'], data['actions']
            )
            
            ratio = torch.exp(log_probs - data['log_probs'])
            policy_loss = -torch.min(
                ratio * advantages,
                torch.clamp(ratio, 0.8, 1.2) * advantages
            ).mean()
            
            # Value loss
            value_loss = F.mse_loss(values, data['rewards'])
            
            # Entropy loss
            entropy_loss = -entropy.mean() * 0.01
            
            # Total loss
            total_loss = policy_loss + 0.5 * value_loss + entropy_loss
            
            # Optimize
            optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(network.parameters(), 0.5)
            optimizer.step()
            
            policy_losses[agent_id] = total_loss.item()
        
        return policy_losses
    
    def _train_shared_critic(self, batch_data: Dict[str, Dict[str, torch.Tensor]]) -> float:
        """Train shared critic network"""
        if not batch_data:
            return 0.0
        
        # Aggregate global states
        global_states = []
        target_values = []
        
        agent_ids = list(batch_data.keys())
        min_batch_size = min(len(data['states']) for data in batch_data.values())
        
        for i in range(min_batch_size):
            # Concatenate states from all agents
            global_state = torch.cat([
                batch_data[agent_id]['states'][i] 
                for agent_id in agent_ids
            ])
            global_states.append(global_state)
            
            # Target value (mean of all agent rewards)
            target_value = torch.stack([
                batch_data[agent_id]['rewards'][i] 
                for agent_id in agent_ids
            ])
            target_values.append(target_value)
        
        global_states = torch.stack(global_states)
        target_values = torch.stack(target_values)
        
        # Forward pass
        predicted_values, _ = self.shared_critic(global_states)
        
        # Value loss
        value_loss = F.mse_loss(predicted_values, target_values)
        
        # Optimize
        self.critic_optimizer.zero_grad()
        value_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.shared_critic.parameters(), 0.5)
        self.critic_optimizer.step()
        
        return value_loss.item()
    
    def _update_coordination_matrix(self, batch_data: Dict[str, Dict[str, torch.Tensor]]):
        """Update coordination matrix based on performance"""
        if len(batch_data) < 2:
            return
        
        # Simple update rule: increase coordination weights for agents with similar rewards
        agent_ids = list(batch_data.keys())
        
        for i, agent_i in enumerate(agent_ids):
            for j, agent_j in enumerate(agent_ids):
                if i != j:
                    reward_similarity = torch.cosine_similarity(
                        batch_data[agent_i]['rewards'].unsqueeze(0),
                        batch_data[agent_j]['rewards'].unsqueeze(0)
                    )
                    
                    # Update coordination matrix
                    learning_rate = 0.01
                    self.coordination_matrix[i, j] += learning_rate * reward_similarity
        
        # Keep matrix values in reasonable range
        self.coordination_matrix = torch.clamp(self.coordination_matrix, -1.0, 1.0)
    
    def reset_hidden_states(self):
        """Reset LSTM hidden states"""
        self.agent_hidden_states.clear()
        self.critic_hidden_state = None
    
    def save_models(self, filepath: str):
        """Save all models"""
        checkpoint = {
            'policy_networks': {
                agent_id: network.state_dict() 
                for agent_id, network in self.policy_networks.items()
            },
            'shared_critic': self.shared_critic.state_dict(),
            'coordination_matrix': self.coordination_matrix,
            'training_stats': dict(self.training_stats)
        }
        torch.save(checkpoint, filepath)
    
    def load_models(self, filepath: str):
        """Load all models"""
        checkpoint = torch.load(filepath, map_location=self.device)
        
        for agent_id, state_dict in checkpoint['policy_networks'].items():
            if agent_id in self.policy_networks:
                self.policy_networks[agent_id].load_state_dict(state_dict)
        
        self.shared_critic.load_state_dict(checkpoint['shared_critic'])
        self.coordination_matrix = checkpoint['coordination_matrix']
        
        if 'training_stats' in checkpoint:
            for key, values in checkpoint['training_stats'].items():
                self.training_stats[key] = deque(values, maxlen=1000)
    
    def get_training_stats(self) -> Dict[str, float]:
        """Get training statistics"""
        stats = {}
        
        for key, values in self.training_stats.items():
            if values:
                stats[f'avg_{key}'] = np.mean(values)
                stats[f'recent_{key}'] = np.mean(list(values)[-100:]) if len(values) >= 100 else np.mean(values)
        
        return stats

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

# Example usage
if __name__ == "__main__":
    # Configuration
    agent_configs = {
        'agent_1': NetworkConfig(input_size=20, hidden_size=128),
        'agent_2': NetworkConfig(input_size=20, hidden_size=128),
        'agent_3': NetworkConfig(input_size=20, hidden_size=128),
        'agent_4': NetworkConfig(input_size=20, hidden_size=128)
    }
    
    action_space_sizes = {
        'agent_1': 5,
        'agent_2': 5,
        'agent_3': 5,
        'agent_4': 5
    }
    
    coordination_config = {
        'enable_coordination': True,
        'buffer_size': 10000
    }
    
    # Initialize coordinator
    coordinator = MultiAgentCoordinatorAdvanced(
        agent_configs, action_space_sizes, coordination_config
    )
    
    # Test with sample observations
    observations = {
        'agent_1': torch.randn(20),
        'agent_2': torch.randn(20),
        'agent_3': torch.randn(20),
        'agent_4': torch.randn(20)
    }
    
    # Get actions
    actions_info = coordinator.get_actions(observations, training=False)
    
    print("Agent actions:")
    for agent_id, info in actions_info.items():
        print(f"{agent_id}: action={info['action'].item()}, value={info['value'].item():.3f}")
    
    print(f"\nCoordination matrix shape: {coordinator.coordination_matrix.shape}")
    print(f"Experience buffer size: {len(coordinator.experience_buffer)}")
    
    # Test training (would need proper experiences)
    print(f"Training stats: {coordinator.get_training_stats()}")