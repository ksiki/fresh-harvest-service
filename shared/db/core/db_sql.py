import logging
from contextlib import asynccontextmanager
from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.common_config import settings

logger = logging.getLogger(__name__)


class SQLClient:
    __slots__ = ("_engine", "_session_factory")

    def __init__(self, url: str, echo: bool = False) -> None:
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session_dependency(self) -> AsyncSession:
        async with self._session_factory() as session:
            try:
                yield session
                logger.info("Postgre session created successfully")
                await session.commit()
                logger.info("Postgre session commit successfully")
            except Exception as e:
                await session.rollback()
                logger.exception(f"Unexpected error in Postgre session lifecycle: {e}")
                raise
            finally:
                logger.info("Postgre session context closed")
                await session.close()

    async def dispose(self) -> None:
        await self._engine.dispose()


database: Final[SQLClient] = SQLClient(url=settings.database_url, echo=settings.debug)
