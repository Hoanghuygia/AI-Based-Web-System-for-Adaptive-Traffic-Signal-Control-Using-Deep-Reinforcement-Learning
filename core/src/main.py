from fastapi import FastAPI, status
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
# from starlette.status import Status

from src.core.config import settings
from src.core.errors import http_422_error_handler, http_error_handler
from src.db.mongodb_utils import close_mongo_connection, open_mongo_connection

app = FastAPI(title=settings.PROJECT_NAME)

if not settings.ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", open_mongo_connection)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

@app.get("/")
async def root():
    return {"message": "hello new world"}
