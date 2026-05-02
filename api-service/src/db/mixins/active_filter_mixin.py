from typing import Generic, TypeVar

from sqlalchemy import select

M = TypeVar("M")


class ActiveFilterMixin(Generic[M]):
    async def get_all_entities(self, only_active: bool = True) -> list[M]:
        stmt = select(self.model)
        if only_active:
            stmt = stmt.where(self.model.is_active == True)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
