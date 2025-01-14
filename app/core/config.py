from typing import List, Optional

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='env.sh', env_file_encoding='utf-8')

    DEBUG: Optional[bool] = False
    TEST: Optional[bool] = False

    PROJECT_NAME: str = 'Bet software bet provider'
    API_V1_STR: str = "/bet/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/bet/docs'

    LINE_HOST: Optional[str] = 'backend-line:8000'

    RABBITMQ_HOST: Optional[str] = 'rabbitmq'
    RABBITMQ_PORT: Optional[int] = 5672
    RABBITMQ_USER: Optional[str] = 'guest'
    RABBITMQ_PASSWORD: Optional[str] = 'guest'


    TEST_POSTGRES_HOST: Optional[str] = 'postgres'
    TEST_POSTGRES_DB: Optional[str] = 'postgres'

    POSTGRES_DB: Optional[str] = 'postgres'
    POSTGRES_USER: Optional[str] = 'postgres'
    POSTGRES_HOST: Optional[str] = 'postgres'
    POSTGRES_PASSWORD: Optional[str] = 'postgres'

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


configs = Settings()


tags_metadata = [
    {
        "name": "event",
        "description": "Events</br>",
    },
]



