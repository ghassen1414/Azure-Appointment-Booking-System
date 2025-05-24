import os
from dotenv import load_dotenv
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings # Changed from pydantic.BaseSettings

# Load .env file from the backend directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key_if_not_set")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        # If you are not using a .env file for some reason for specific variables,
        # you can enable reading from system environment vars like this:
        # env_file = ".env" # pydantic-settings will try to load this by default
        # env_file_encoding = 'utf-8'


settings = Settings()