from fastapi import APIRouter

from .endpoints.authentication import router as Authentication_route
from .endpoints.user import router as User_route

routers = APIRouter()

routers.include_router(Authentication_route)
routers.include_router(User_route)