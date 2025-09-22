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

from ..configs.network_config import NetworkConfig
from ..agents.lstm_policy import LSTMPolicyNetwork
from ..agents.share_critic_network import SharedCriticNetwork
from ..utils.experience_buffer import ExperienceBuffer, Experience

class MultiAgentCoordinatorAdvanced:
    """Advanced Multi-Agent Coordinator với centralized training"""
    
    def __init__(self, 
                 agent_configs: Dict[str, NetworkConfig], #Agent configurations is a dic of all agents configurations
                 action_space_sizes: Dict[str, int],
                 coordination_config: Dict[str, Any]):
        
        self.agent_configs = agent_configs
        self.action_space_sizes = action_space_sizes
        self.coordination_config = coordination_config
        self.device = list(agent_configs.values())[0].device # take the the device of the first agent config as the default for system

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
        shared_config = list(agent_configs.values())[0] # use the first agent config as the shared config

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
            'value_losses': deque(maxlen=1000), # loss for xritic layer
            'entropy_losses': deque(maxlen=1000), # the level of randomness action, show if the agent is exploring or exploiting
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