from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Stonksense API"
    
    class Config:
        env_file = ".env"