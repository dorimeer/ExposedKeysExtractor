from typing import Any

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    GITHUB_TOKENS: Any
    SEARCH_KEYWORDS: Any

    @validator('GITHUB_TOKENS', pre=True)
    def validate_github_tokens(cls, value: str) -> list[str]:
        return value.split(';')

    @validator('SEARCH_KEYWORDS', pre=True)
    def validate_search_keywords(cls, value: str) -> list[str]:
        return value.split(';')

    class Config:
        case_sensitive = True
        env_file = "../.env"
        env_file_encoding = 'utf-8'


settings = Settings()
