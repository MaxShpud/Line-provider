from typing import Any
from dotenv import find_dotenv, load_dotenv

from pydantic import PostgresDsn, BaseModel, AnyHttpUrl
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv('../.env'))

class DBConfig(BaseModel):
    app_name: str
    dsn: PostgresDsn
    pool_size: int
    timezone: str
    max_overflow: int
    pool_pre_ping: bool
    connection_timeout: int
    command_timeout: int
    server_settings: dict[str, Any] = {}
    connect_args: dict[str, Any] = {}
    debug: bool

class ArqRedisConfig(BaseModel):
    host: str
    port: int
    password: str
    caching_time: int

class BetClientConfig(BaseModel):
    name: str
    base_url: AnyHttpUrl
    retries_enabled: bool

class Config(BaseSettings):
    DB: DBConfig
    ARQ_REDIS: ArqRedisConfig
    BET_CLIENT: BetClientConfig

    class Config:
        env_file = "../../.env"
        env_nested_delimiter = "__"
        validate_assignment = True
