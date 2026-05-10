import logging

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.exceptions import UserAlreadyExists, UserNotExists
from shared.db.models.user import User
from shared.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User, AsyncSession]):
    model = User

    async def get_id_by_tg_id(self, tg_id: int) -> int | None:
        stmt = select(User.id).where(User.tg_id == tg_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def register(self, tg_id: int) -> int:
        try:
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
            return result.scalar_one()
        except IntegrityError:
            raise UserAlreadyExists()

    async def update_last_activity(self, user_id: int) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(last_activity=func.now())
            .returning(User.id)
        )
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none() is None:
            raise UserNotExists()
