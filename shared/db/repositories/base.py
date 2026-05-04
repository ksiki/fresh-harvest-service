from typing import Generic, Type, TypeVar

from aiobotocore.client import AioBaseClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models.base import BaseModel

T = TypeVar("T", bound=AsyncSession | AioBaseClient)
M = TypeVar("M", bound=BaseModel)


class BaseRepository(Generic[M, T]):
    __slots__ = ("_session",)
    model: Type[M]

    def __init__(self, session: T):
        self._session = session

    @property
    def session(self) -> T:
        return self._session

    async def get_by_id(self, id: int) -> M | None:
        return await self.session.get(self.model, id)

    async def delete_by_id(self, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
