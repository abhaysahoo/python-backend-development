from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# setting up validation for environment variables
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    BACKEND_CORS_ORIGINS: list[str]

try:
    settings = Settings()
except ValidationError as e:
    print(e)
    raise