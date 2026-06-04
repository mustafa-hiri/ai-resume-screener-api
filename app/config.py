from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-nano"

    class Config:
        env_file = ".env"


settings = Settings()