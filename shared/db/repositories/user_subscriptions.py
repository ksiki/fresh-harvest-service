import logging
from datetime import timedelta

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models.user_subscription import UserSubscription
from shared.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class UserSubscriptionRepository(BaseRepository[UserSubscription, AsyncSession]):
    model = UserSubscription

    async def get_active(self, user_id: int) -> UserSubscription | None:
        """Всегда должно возвращать подписку, если пользователь существует (без None)
        т.к. сторонний воркер для обслуживания БД следит за тем,
        что при окончании подписки, дает пользователю бесплатную"""

        stmt = (
            select(UserSubscription)
            .where(
                UserSubscription.user_id == user_id, UserSubscription.is_active == True
            )
            .order_by(UserSubscription.expires_at.desc())
            .limit(limit=1)
        )
        result = await self.session.execute(stmt)
        logger.info("Get active user subsctiprion completed successfully.")
        return result.scalar_one()

    async def subscribe(self, user_id: int, sub_id: int, duration: timedelta) -> int:
        disable_stmt = (
            update(UserSubscription)
            .where(
                UserSubscription.user_id == user_id, UserSubscription.is_active == True
            )
            .values(expires_at=func.now(), is_active=False)
        )
        await self.session.execute(disable_stmt)
        logger.info("Disable all old user subscriptions completed successfully.")

        insert_stmt = (
            insert(UserSubscription)
            .values(
                user_id=user_id,
                subscription_id=sub_id,
                purchase_at=func.now(),
                expires_at=func.now() + duration,
                is_active=True,
            )
            .returning(UserSubscription.id)
        )
        result = await self.session.execute(insert_stmt)
        logger.info("Subscribe user completed successfully.")
        return result.scalar_one_or_none()

    async def deactivate_expired_subscriptions(self) -> list[int]:
        stmt = (
            update(UserSubscription)
            .where(
                UserSubscription.is_active == True,
                UserSubscription.expires_at < func.now(),
            )
            .values(is_active=False)
            .returning(UserSubscription.user_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def bulk_subscribe_free(
        self, user_ids: list[int], free_sub_id: int, duration: timedelta
    ) -> None:
        stmt = insert(UserSubscription).values(
            [
                {
                    "user_id": u_id,
                    "subscription_id": free_sub_id,
                    "purchase_at": func.now(),
                    "expires_at": func.now() + duration,
                    "is_active": True,
                }
                for u_id in user_ids
            ]
        )
        await self.session.execute(stmt)
