from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "RagApp"
    APP_VERSION: str = "1.0.0"
    FILE_ALLOWED_TYPES: list[str] = ["text/plain" , "application/pdf"]
    FILE_MAX_SIZE_MB: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 512000
    FILE_PROCESSING_TRIGGERED: str = "file_processing_triggered"
    class Config : SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

def get_settings() -> Settings:
    return Settings()