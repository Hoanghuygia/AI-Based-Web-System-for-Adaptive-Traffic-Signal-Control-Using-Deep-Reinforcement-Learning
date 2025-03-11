from fastapi import APIRouter

from .endpoints.authentication import router as Authentication_route

routers = APIRouter()

routers.include_router(Authentication_route)