from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    MODE: str = 'DEV'

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_POOL_RECYCLE: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CACHING_TIME: int
    # GET_EVENTS_URL: str
    # GET_SINGLE_EVENT_URL: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


load_dotenv(find_dotenv('.env'))
config = Config()
