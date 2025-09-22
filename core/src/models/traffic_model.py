from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class SimulationStatus(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

class TrafficSimulationRequest(BaseModel):
    network_file: str
    route_file: str
    simulation_time: int = 3600
    use_gui: bool = False
    reward_function: str = "queue"

class TrafficSimulationResponse(BaseModel):
    simulation_id: str
    status: SimulationStatus
    current_step: int
    total_reward: float
    traffic_lights_state: Dict[str, str]

class TrafficMetrics(BaseModel):
    simulation_id: str
    step: int
    waiting_time: float
    queue_length: int
    throughput: int
    reward: float
    timestamp: str