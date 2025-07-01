class MultiAgentCoordinator:
    """Coordinator quản lý toàn bộ multi-agent system"""
    
    def __init__(self, network_topology: Dict[str, List[str]]):
        self.network_topology = network_topology
        self.agents = {}
        self.communication_protocol = CommunicationProtocol()
        self.global_state = {}
        self.coordination_history = deque(maxlen=1000)
        
    def create_agents(self, intersections_config: Dict[str, Dict[str, Any]]):
        """Tạo tất cả agents cho các intersections"""
        for intersection_id, config in intersections_config.items():
            agent_id = f"agent_{intersection_id}"
            
            # Get neighboring agents
            neighboring_agents = []
            for neighbor_intersection in self.network_topology.get(intersection_id, []):
                neighboring_agents.append(f"agent_{neighbor_intersection}")
            
            # Create agent
            agent = IntersectionAgent(
                agent_id=agent_id,
                intersection_id=intersection_id,
                position=config['position'],
                neighboring_agents=neighboring_agents,
                state_space_config=config.get('state_space', {}),
                action_space_config=config.get('action_space', {})
            )
            
            self.agents[agent_id] = agent
            self.communication_protocol.register_agent(agent)
    
    def get_all_observations(self, raw_states: Dict[str, Dict[str, Any]], 
                           use_global_obs: bool = False) -> Dict[str, np.ndarray]:
        """Lấy observations cho tất cả agents"""
        observations = {}
        
        for agent_id, agent in self.agents.items():
            intersection_id = agent.intersection_id
            if intersection_id in raw_states:
                if use_global_obs:
                    obs = agent.get_global_observation(raw_states[intersection_id])
                else:
                    obs = agent.get_local_observation(raw_states[intersection_id])
                observations[agent_id] = obs
        
        return observations
    
    def coordinate_actions(self, proposed_actions: Dict[str, int]) -> Dict[str, int]:
        """Coordinate actions giữa các agents"""
        coordinated_actions = proposed_actions.copy()
        
        # Simple coordination: avoid conflicts between neighboring agents
        for agent_id, action in proposed_actions.items():
            agent = self.agents[agent_id]
            
            # Check for conflicts with neighbors
            for neighbor_id in agent.neighboring_agents:
                if neighbor_id in proposed_actions:
                    neighbor_action = proposed_actions[neighbor_id]
                    
                    # Resolve conflicts (simple priority-based)
                    if self._actions_conflict(action, neighbor_action):
                        # Agent with higher priority keeps their action
                        if agent_id < neighbor_id:  # Simple priority rule
                            coordinated_actions[neighbor_id] = 0  # KEEP_CURRENT_PHASE
        
        return coordinated_actions
    
    def _actions_conflict(self, action1: int, action2: int) -> bool:
        """Kiểm tra xem 2 actions có conflict không"""
        # Both agents trying to switch phases simultaneously
        switching_actions = [1, 2]  # SWITCH_TO_NS_GREEN, SWITCH_TO_EW_GREEN
        return action1 in switching_actions and action2 in switching_actions
    
    def update_system_state(self, rewards: Dict[str, float], 
                          coordination_success: Dict[str, bool]):
        """Cập nhật trạng thái toàn hệ thống"""
        for agent_id, agent in self.agents.items():
            if agent_id in rewards:
                agent.update_performance(
                    rewards[agent_id], 
                    coordination_success.get(agent_id, False)
                )
        
        # Process communications
        self.communication_protocol.process_outgoing_messages()
        
        # Record coordination history
        self.coordination_history.append({
            'timestamp': time.time(),
            'avg_reward': np.mean(list(rewards.values())),
            'coordination_rate': np.mean(list(coordination_success.values()))
        })
    
    def get_system_metrics(self) -> Dict[str, float]:
        """Lấy metrics của toàn hệ thống"""
        if len(self.coordination_history) == 0:
            return {
                'avg_system_reward': 0.0,
                'coordination_success_rate': 0.0,
                'communication_efficiency': 0.0
            }
        
        recent_history = list(self.coordination_history)[-100:]
        
        return {
            'avg_system_reward': np.mean([h['avg_reward'] for h in recent_history]),
            'coordination_success_rate': np.mean([h['coordination_rate'] for h in recent_history]),
            'communication_efficiency': self._calculate_communication_efficiency()
        }
    
    def _calculate_communication_efficiency(self) -> float:
        """Tính hiệu quả communication"""
        total_messages = sum(len(agent.message_queue) for agent in self.agents.values())
        total_agents = len(self.agents)
        
        if total_agents == 0:
            return 0.0
        
        # Normalize by number of agents
        return min(total_messages / (total_agents * 10), 1.0)