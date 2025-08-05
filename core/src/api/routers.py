from fastapi import APIRouter

from .endpoints.authentication import router as Authentication_route
from .endpoints.user import router as User_route
from .endpoints.sumo import router as Sumo_route
from .endpoints.ws_sumo import router as SumoWebSocket_route
from .endpoints.traffic_simulation import router as traffic_simulation

routers = APIRouter()

routers.include_router(Authentication_route)
routers.include_router(User_route)
routers.include_router(Sumo_route)
routers.include_router(SumoWebSocket_route)
routers.include_router(traffic_simulation.router, prefix="/traffic", tags=["traffic"])