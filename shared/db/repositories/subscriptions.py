import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.exceptions import SubscriptionNotFoundError
from shared.db.mixins.active_filter_mixin import ActiveFilterMixin
from shared.db.mixins.str_id_mixin import StrIdMixin
from shared.db.models.subscription import Subscription
from shared.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class SubscriptionRepository(
    BaseRepository[Subscription, AsyncSession],
    ActiveFilterMixin[Subscription],
    StrIdMixin[Subscription],
):
    model = Subscription

    async def get_free_subscription(self) -> Subscription:
        stmt = (
            select(Subscription)
            .where(Subscription.str_id.ilike("%free%"), Subscription.is_active == True)
            .order_by(Subscription.id)
            .limit(limit=1)
        )
        result = await self.session.execute(stmt)
        sub = result.scalar_one_or_none()

        if not sub:
            raise SubscriptionNotFoundError()

        return sub

    async def create_or_update(
        self,
        str_id: str,
        title: str,
        active_post_limit: int,
        post_lifetime_hours: int,
        duration_days: int,
        price: float,
        is_active: bool,
    ) -> None:
        logger.info("Create or update subscription")
        stmt = insert(Subscription).values(
            str_id=str_id,
            title=title,
            active_post_limit=active_post_limit,
            post_lifetime_hours=post_lifetime_hours,
            duration_days=duration_days,
            price=price,
            is_active=is_active,
        )
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=["str_id"],
            set_={
                "title": stmt.excluded.title,
                "active_post_limit": stmt.excluded.active_post_limit,
                "post_lifetime_hours": stmt.excluded.post_lifetime_hours,
                "duration_days": stmt.excluded.duration_days,
                "price": stmt.excluded.price,
                "is_active": stmt.excluded.is_active,
            },
        )
        await self.session.execute(upsert_stmt)
