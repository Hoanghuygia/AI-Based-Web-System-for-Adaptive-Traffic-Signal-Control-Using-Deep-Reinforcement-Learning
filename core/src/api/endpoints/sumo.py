from fastapi import APIRouter
from src.controllers.traffic_controller import (
    set_traffic_light_phase,
    get_traffic_light_phase
)

router = APIRouter()

@router.post("/traffic-light/{light_id}/phase/{phase}")
async def change_traffic_light_phase(light_id: str, phase: int):
    success = await set_traffic_light_phase(light_id, phase)
    if success:
        return {"status": "ok", "light_id": light_id, "new_phase": phase}
    return {"status": "error", "message": "Failed to change traffic light phase"}

@router.get("/traffic-light/{light_id}/phase")
async def get_traffic_light_phase_api(light_id: str):
    current_phase = await get_traffic_light_phase(light_id)
    if current_phase == -1:
        return {"status": "error", "message": "Could not fetch current phase"}
    return {"status": "ok", "light_id": light_id, "current_phase": current_phase}

