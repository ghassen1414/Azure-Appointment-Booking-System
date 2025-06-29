import os
from dotenv import load_dotenv
from typing import List, Union # Ensure Union is imported
from pydantic import AnyHttpUrl, field_validator # field_validator for Pydantic v2
from pydantic_settings import BaseSettings

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key_if_not_set")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    ACS_CONNECTION_STRING: str = os.getenv("ACS_CONNECTION_STRING", "") # From previous steps
    ACS_SENDER_ADDRESS: str = os.getenv("ACS_SENDER_ADDRESS", "")   # From previous steps

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [] # Default to empty list

    #@field_validator("BACKEND_CORS_ORIGINS", mode='before') # mode='before' for Pydantic v2
    @classmethod # Add classmethod decorator
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and v.strip(): # Check if string is not empty
            # Ensure no leading/trailing whitespace on individual origins
            return [item.strip() for item in v.split(",")]
        elif isinstance(v, list):
            return v
        return [] # Return empty list if input is invalid or empty string

    class Config:
        case_sensitive = True
        # env_file = ".env" # pydantic-settings loads .env by default if it exists

settings = Settings()