import traci
from ..services.sumo_service import SUMOService
from ..models.traffic_models import TrafficSimulationRequest, TrafficSimulationResponse

async def set_traffic_light_phase(light_id: str, phase_index: int) -> bool:
    try:
        traci.trafficlight.setPhase(light_id, phase_index)
        return True
    except Exception as e:
        print(f"[ERROR] set_traffic_light_phase: {e}")
        return False

async def get_traffic_light_phase(light_id: str) -> int:
    try:
        return traci.trafficlight.getPhase(light_id)
    except Exception as e:
        print(f"[ERROR] get_traffic_light_phase: {e}")
        return -1
    
class TrafficController:
    def __init__(self):
        self.sumo_service = SUMOService()
    
    async def create_simulation(self, request: TrafficSimulationRequest) -> TrafficSimulationResponse:
        """Create new traffic simulation"""
        simulation_id = await self.sumo_service.create_simulation(
            network_file=request.network_file,
            route_file=request.route_file,
            simulation_time=request.simulation_time,
            use_gui=request.use_gui
        )
        
        return TrafficSimulationResponse(
            simulation_id=simulation_id,
            status="stopped",
            current_step=0,
            total_reward=0.0,
            traffic_lights_state={}
        )
    
    async def start_simulation(self, simulation_id: str):
        """Start simulation"""
        success = await self.sumo_service.start_simulation(simulation_id)
        if not success:
            raise Exception("Failed to start simulation")
        
        return await self.sumo_service.get_simulation_status(simulation_id)

