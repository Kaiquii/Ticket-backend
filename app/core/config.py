from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:4343@localhost:5432/ticket_db"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 4320
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:4200",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:4200",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
