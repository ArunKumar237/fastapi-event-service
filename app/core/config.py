from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "event-service"

    database_url: str
    redis_url: str
    API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
