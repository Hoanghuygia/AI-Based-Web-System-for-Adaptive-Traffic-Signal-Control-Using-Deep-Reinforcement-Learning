from dataclasses import dataclass
import torch

@dataclass
class NetworkConfig:
    """Configuration cho neural networks"""
    input_size: int
    hidden_size: int = 128
    num_layers: int = 2
    dropout: float = 0.1
    learning_rate: float = 3e-4
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
