import logging

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.base_rep import BaseRepository
from shared.db.models.user import User

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User, AsyncSession]):
    model = User

    async def get_id_by_tg_id(self, tg_id: int) -> int | None:
        stmt = select(User.id).where(User.tg_id == tg_id)
        result = await self.session.execute(stmt)
        logger.info("Fetched id by tg id completed successfully.")
        return result.scalar_one_or_none()

    async def register(self, tg_id: int) -> int:
        stmt = (
            insert(User)
            .values(
                tg_id=tg_id,
                first_activity=func.now(),
                last_activity=func.now(),
            )
            .returning(User.id)
        )
        result = await self.session.execute(stmt)
        logger.info("Register new user completed successfully.")
        return result.scalar_one()

    async def update_last_activity(self, tg_id: int) -> None:
        stmt = update(User).where(User.tg_id == tg_id).values(last_activity=func.now())
        await self.session.execute(stmt)
        logger.info("Update last activity completed successfully.")
