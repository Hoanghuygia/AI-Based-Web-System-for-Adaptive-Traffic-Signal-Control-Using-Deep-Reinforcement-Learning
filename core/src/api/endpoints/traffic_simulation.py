from fastapi import APIRouter, HTTPException, Depends
from ...controllers.traffic_controller import TrafficController
from ...models.traffic_models import TrafficSimulationRequest, TrafficSimulationResponse

router = APIRouter()
traffic_controller = TrafficController()

@router.post("/simulations", response_model=TrafficSimulationResponse)
async def create_simulation(request: TrafficSimulationRequest):
    """Create new traffic simulation"""
    try:
        return await traffic_controller.create_simulation(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulations/{simulation_id}/start")
async def start_simulation(simulation_id: str):
    """Start traffic simulation"""
    try:
        return await traffic_controller.start_simulation(simulation_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/simulations/{simulation_id}/status")
async def get_simulation_status(simulation_id: str):
    """Get simulation status"""
    status = await traffic_controller.sumo_service.get_simulation_status(simulation_id)
    if not status:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return status

@router.post("/simulations/{simulation_id}/step")
async def step_simulation(simulation_id: str, action: int = None):
    """Execute simulation step"""
    try:
        return await traffic_controller.sumo_service.step_simulation(simulation_id, action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))