from pathlib import Path

from pydantic import BaseModel, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: MySQLDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class AuthJWT(BaseModel):
    public_path: Path = BASE_DIR / "certs" / "public.pem"
    private_path: Path = BASE_DIR / "certs" / "private.pem"
    algorithm: str = "RS256"
    token_expire_minutes: int = 30
    resfresh_token_expire_days: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template",".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    ) 
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthJWT = AuthJWT()

    
settings = Settings()  # type: ignore