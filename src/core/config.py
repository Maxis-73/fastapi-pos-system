from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # App
    APP_NAME: str = "POS System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A simple point-of-sale system"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()