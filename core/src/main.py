from fastapi import FastAPI, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.simulator.sumo_manager import SUMOManager
from src.core.config import settings
from src.core.errors import http_422_error_handler, http_error_handler
from src.db.mongodb_utils import close_mongo_connection, open_mongo_connection
from src.api.routers import routers

sumo_manager = SUMOManager(sumo_cfg_path="data/map.sumocfg")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_mongo_connection()
    sumo_manager.start()

    yield
    
    await close_mongo_connection()
    sumo_manager.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

if not settings.ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(routers, prefix=settings.API_VERSION_1)

@app.get("/", tags=["root"])
async def root():
    return {"message": "hello new world"}

