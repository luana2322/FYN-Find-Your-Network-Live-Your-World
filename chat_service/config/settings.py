from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="chat-service", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8080, alias="APP_PORT")

    mongo_uri: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    mongo_db_name: str = Field(default="chat_service", alias="MONGO_DB_NAME")

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    jwt_secret: str = Field(default="replace_me", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_audience: str = Field(default="chat-service", alias="JWT_AUDIENCE")
    jwt_issuer: str = Field(default="auth-service", alias="JWT_ISSUER")

    fcm_server_key: str | None = Field(default=None, alias="FCM_SERVER_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True


@lru_cache
essential_settings = Settings()  # instantiate once for import-time failures

def get_settings() -> Settings:
    return essential_settings
