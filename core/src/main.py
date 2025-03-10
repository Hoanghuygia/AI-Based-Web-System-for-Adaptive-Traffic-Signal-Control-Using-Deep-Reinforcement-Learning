from fastapi import FastAPI, status
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

# from core.core.config import settings
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(CORSMiddleware)


@app.get("/")
async def root():
    return {"message": "hello new world"}
