import traci

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

