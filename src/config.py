from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    app_name: str = "Phase 1 Practice API"
    openai_api_key: str  # required
    openai_model: str = "gpt-4o-mini"
    max_tokens: int = 1000
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump(exclude={"openai_api_key"}))
