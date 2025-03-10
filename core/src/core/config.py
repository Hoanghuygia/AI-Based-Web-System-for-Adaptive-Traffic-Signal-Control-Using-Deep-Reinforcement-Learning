import os

from pydantic_settings import BaseSettings
from starlette.datastructures import CommaSeparatedStrings

class Settings(BaseSettings):
    PROJECT_NAME: str
    ALLOWED_HOSTS: CommaSeparatedStrings = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
    MONGODB_URL: str  
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10
    DB_NAME: str     
    SECRET_KEY: str   
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()