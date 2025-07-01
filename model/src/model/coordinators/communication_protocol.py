class CommunicationProtocol:
    """Protocol quản lý communication giữa các agents"""
    
    def __init__(self, max_message_delay: float = 0.1, 
                 max_broadcast_frequency: float = 2.0):
        self.max_message_delay = max_message_delay
        self.max_broadcast_frequency = max_broadcast_frequency
        self.message_buffer = deque(maxlen=1000)
        self.agents = {}
        self.last_broadcast_time = {}
        
    def register_agent(self, agent: IntersectionAgent):
        """Đăng ký agent vào protocol"""
        self.agents[agent.agent_id] = agent
        self.last_broadcast_time[agent.agent_id] = 0
    
    def route_message(self, message: AgentMessage):
        """Route message đến đích"""
        # Add realistic communication delay
        time.sleep(np.random.uniform(0, self.max_message_delay))
        
        if message.receiver_id == "ALL":
            # Broadcast message
            for agent_id, agent in self.agents.items():
                if agent_id != message.sender_id:
                    agent.receive_message(message)
        else:
            # Direct message
            if message.receiver_id in self.agents:
                self.agents[message.receiver_id].receive_message(message)
    
    def process_outgoing_messages(self):
        """Xử lý tất cả outgoing messages"""
        for agent in self.agents.values():
            while agent.outgoing_messages:
                message = agent.outgoing_messages.popleft()
                
                # Check broadcast frequency limit
                if (message.message_type == MessageType.STATE_BROADCAST and 
                    message.receiver_id == "ALL"):
                    current_time = time.time()
                    last_broadcast = self.last_broadcast_time.get(message.sender_id, 0)
                    
                    if current_time - last_broadcast < 1.0 / self.max_broadcast_frequency:
                        continue  # Skip this broadcast
                    
                    self.last_broadcast_time[message.sender_id] = current_time
                
                self.route_message(message)