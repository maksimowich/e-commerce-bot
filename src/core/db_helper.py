from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.core.config import app_settings
from src.utils.backoff import backoff


class DatabaseHelper:
    def __init__(
            self,
            url,
            echo: bool,
            echo_pool: bool,
            max_overflow: int = 10,
            pool_size: int = 5,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )

        self.async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            await session.execute(text(f"SET search_path TO {app_settings.postgres.schema_}"))
            yield session

    @backoff()
    async def check_connection(self):
        try:
            async with self.engine.begin() as conn:
                res = await conn.execute(text("SELECT 1"))
                res.scalar()
                logger.info("Connected to Postgres")
        except Exception as e:
            logger.info("Cannot connect to Postgres")
            raise e


db_helper = DatabaseHelper(
    url=app_settings.postgres.async_url,
    echo=app_settings.postgres.echo,
    echo_pool=app_settings.postgres.echo_pool,
    max_overflow=app_settings.postgres.max_overflow,
    pool_size=app_settings.postgres.pool_size,
)
