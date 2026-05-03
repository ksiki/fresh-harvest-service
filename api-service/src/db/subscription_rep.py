import logging

from db.core.base_rep import BaseRepository
from db.mixins.active_filter_mixin import ActiveFilterMixin
from db.mixins.str_id_mixin import StrIdMixin
from db.models.subscription import Subscription
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class SubscriptionRepository(
    BaseRepository[Subscription, AsyncSession],
    ActiveFilterMixin[Subscription],
    StrIdMixin[Subscription],
):
    model = Subscription

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
