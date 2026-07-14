from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Workflow Assistant"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"


settings = Settings()
