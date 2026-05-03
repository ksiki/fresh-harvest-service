from typing import Generic, Type, TypeVar, Union

from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Union[AsyncSession, AioBaseClient])
M = TypeVar("M")


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
