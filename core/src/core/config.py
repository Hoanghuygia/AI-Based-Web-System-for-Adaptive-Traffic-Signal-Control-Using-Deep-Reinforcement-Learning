import os

from pydantic_settings import BaseSettings
from starlette.datastructures import CommaSeparatedStrings

class Settings(BaseSettings):
    PROJECT_NAME: str
    ALLOWED_HOSTS: CommaSeparatedStrings = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
    MONGODB_URL: str  
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10
    DB_NAME: str = "data"   
    USER_COLLECTION_NAME: str = "users" 
    SECRET_KEY: str  =  os.getenv("SECRET_KEY", "")
    API_VERSION_1: str = "/apiv1"  
    # ACCESSS_TOKEN_EXPIRED_TIME: int = 60 * 24 * 7 # token last one week
    ACCESSS_TOKEN_EXPIRED_TIME: int = 15 # token last one minute
    REFRESH_TOKEN_EXPIRED_TIME: int = 15 # token last one minute
    JWT_TOKEN_PREFIX: str = "Token"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()