# backend/config.py (새 파일)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # .env 파일을 읽어오도록 설정
    model_config = SettingsConfigDict(env_file=".env")


# 설정 객체 인스턴스 생성
settings = Settings()
