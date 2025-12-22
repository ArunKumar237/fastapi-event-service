from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "event-service"

    postgres_dsn: str
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings()
