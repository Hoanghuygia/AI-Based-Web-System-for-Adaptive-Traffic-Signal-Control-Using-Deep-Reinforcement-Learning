import numpy as np
from typing import List
from collections import deque, namedtuple
import threading
from collections import namedtuple

Experience = namedtuple('Experience', [
    'state', 'action', 'reward', 'next_state', 'done',
    'hidden_state', 'cell_state', 'log_prob', 'value'
])

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