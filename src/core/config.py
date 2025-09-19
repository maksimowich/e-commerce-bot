from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

uuid_regex = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


class TgConfig(BaseModel):
    bot_token: str


class YookassaConfig(BaseModel):
    account_id: str
    secret_key: str


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    database: str
    schema_: str = Field(alias="schema")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class FormsConfig(BaseModel):
    categories_page_size: int = 3
    subcategories_page_size: int = 5
    products_page_size: int = 4


class Settings(BaseSettings):
    tg: TgConfig
    yookassa: YookassaConfig
    postgres: PostgresConfig
    forms: FormsConfig = FormsConfig()

    excel_filepath: str

    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).resolve().parent.parent.parent / ".env",
            Path(__file__).resolve().parent.parent.parent / ".env.template",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="allow",
    )


app_settings = Settings()
