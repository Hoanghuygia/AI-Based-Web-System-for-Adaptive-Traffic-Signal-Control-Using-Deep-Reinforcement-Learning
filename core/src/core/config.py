from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API for Adaptive Traffic Signal Control Using Deep Reinforcement Learning"
    MONGODB_URL: str  
    DB_NAME: str     
    SECRET_KEY: str   
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()