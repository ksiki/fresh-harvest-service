from typing import Generic, TypeVar

from sqlalchemy import select

M = TypeVar("M")


class StrIdMixin(Generic[M]):
    async def get_by_str_id(self, str_id: str) -> M | None:
        stmt = select(self.model).where(self.model.str_id == str_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
