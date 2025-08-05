import os
import sys
import gym
import sumo_rl
import uuid
from typing import Dict, Optional
from ..models.traffic_models import SimulationStatus, TrafficMetrics

class SUMOService:
    def __init__(self):
        self.active_simulations: Dict[str, dict] = {}
        self._setup_sumo_home()
    
    def _setup_sumo_home(self):
        """Setup SUMO environment"""
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            raise Exception("SUMO_HOME environment variable not set")
    
    async def create_simulation(self, network_file: str, route_file: str, 
                              simulation_time: int = 3600, use_gui: bool = False) -> str:
        """Create new traffic simulation"""
        simulation_id = str(uuid.uuid4())
        
        try:
            env = gym.make('sumo-rl-v0',
                          net_file=f"sumo_data/networks/{network_file}",
                          route_file=f"sumo_data/routes/{route_file}",
                          out_csv_name=f'outputs/simulation_{simulation_id}',
                          use_gui=use_gui,
                          num_seconds=simulation_time)
            
            self.active_simulations[simulation_id] = {
                'env': env,
                'status': SimulationStatus.STOPPED,
                'current_step': 0,
                'total_reward': 0.0,
                'obs': None
            }
            
            return simulation_id
            
        except Exception as e:
            raise Exception(f"Failed to create simulation: {str(e)}")
    
    async def start_simulation(self, simulation_id: str) -> bool:
        """Start or resume simulation"""
        if simulation_id not in self.active_simulations:
            return False
            
        sim = self.active_simulations[simulation_id]
        sim['obs'] = sim['env'].reset()
        sim['status'] = SimulationStatus.RUNNING
        return True
    
    async def step_simulation(self, simulation_id: str, action: Optional[int] = None) -> TrafficMetrics:
        """Execute one simulation step"""
        if simulation_id not in self.active_simulations:
            raise Exception("Simulation not found")
            
        sim = self.active_simulations[simulation_id]
        
        if action is None:
            action = sim['env'].action_space.sample()
        
        obs, reward, done, info = sim['env'].step(action)
        
        sim['obs'] = obs
        sim['current_step'] += 1
        sim['total_reward'] += reward
        
        if done:
            sim['status'] = SimulationStatus.COMPLETED
        
        return TrafficMetrics(
            simulation_id=simulation_id,
            step=sim['current_step'],
            waiting_time=info.get('waiting_time', 0),
            queue_length=info.get('queue_length', 0),
            throughput=info.get('throughput', 0),
            reward=reward,
            timestamp=str(datetime.now())
        )
    
    async def get_simulation_status(self, simulation_id: str) -> dict:
        """Get current simulation status"""
        if simulation_id not in self.active_simulations:
            return None
            
        sim = self.active_simulations[simulation_id]
        return {
            'simulation_id': simulation_id,
            'status': sim['status'],
            'current_step': sim['current_step'],
            'total_reward': sim['total_reward']
        }