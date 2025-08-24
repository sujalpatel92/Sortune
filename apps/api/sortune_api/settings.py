from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SORTUNE_")

    # General
    ENV: str = "dev"

    # Connections
    REDIS_URL: str = "redis://redis:6379/0"  # docker default; use localhost in local runs

    # Optional providers (future)
    OPENAI_API_KEY: str | None = None
    DATABASE_URL: str | None = None


settings = Settings()
