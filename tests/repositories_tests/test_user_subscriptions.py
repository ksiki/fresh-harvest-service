from datetime import datetime, timedelta
from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy import func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models.user_subscription import UserSubscription
from shared.db.repositories.subscriptions import SubscriptionRepository
from shared.db.repositories.user_subscriptions import UserSubscriptionRepository


@pytest_asyncio.fixture
async def subscription(subscription_rep: SubscriptionRepository) -> tuple:
    sub_str_id = "free"
    await subscription_rep.create_or_update(
        str_id=sub_str_id,
        title="Free Sub",
        active_post_limit=3,
        post_lifetime_hours=24,
        duration_days=30,
        price=Decimal("0"),
        is_active=True,
    )
    sub = await subscription_rep.get_by_str_id(sub_str_id)
    return (sub.id, sub.duration_days)


@pytest.mark.asyncio
class TestSubscriptionRep:
    async def test_user_subscribe(
        self,
        user_subscription_rep: UserSubscriptionRepository,
        user_id: int,
        subscription: tuple,
    ) -> None:
        sub_id, duration = subscription

        user_sub_id = await user_subscription_rep.subscribe(
            user_id=user_id,
            sub_id=sub_id,
            duration=timedelta(days=duration),
        )
        user_sub = await user_subscription_rep.get_by_id(id=user_sub_id)

        assert user_sub is not None

    @pytest.mark.parametrize(
        "test_user_id, expires_at, expectation_result",
        [
            (1, func.now() - timedelta(hours=1), UserSubscription),
            (2, func.now() + timedelta(hours=1), UserSubscription),
            (999, func.now() + timedelta(hours=1), type(None)),
        ],
    )
    async def test_get_active(
        self,
        test_user_id: int,
        expires_at: datetime,
        expectation_result: UserSubscription | None,
        session: AsyncSession,
        user_id: int,
        subscription: tuple,
        user_subscription_rep: UserSubscriptionRepository,
    ) -> None:
        sub_id, _ = subscription

        stmt = insert(UserSubscription).values(
            user_id=user_id,
            subscription_id=sub_id,
            purchase_at=func.now(),
            expires_at=expires_at,
            is_active=True,
        )
        await session.execute(stmt)

        sub = await user_subscription_rep.get_active(user_id=test_user_id)

        assert isinstance(sub, expectation_result)

    async def test_deactivate_expired_subscriptions(
        self,
        user_id: int,
        subscription: tuple,
        session: AsyncSession,
        user_subscription_rep: UserSubscriptionRepository,
    ) -> None:
        sub_id, _ = subscription

        stmt = (
            insert(UserSubscription)
            .values(
                user_id=user_id,
                subscription_id=sub_id,
                purchase_at=func.now(),
                expires_at=func.now() - timedelta(hours=1),
                is_active=True,
            )
            .returning(UserSubscription.id)
        )
        result = await session.execute(stmt)
        user_sub_id = result.scalar_one()

        await user_subscription_rep.deactivate_expired_subscriptions()

        user_sub = await user_subscription_rep.get_by_id(id=user_sub_id)
        assert user_sub.is_active is False

    async def test_bulk_subscribe_free(
        self,
        user_id: int,
        subscription: tuple,
        user_subscription_rep: UserSubscriptionRepository,
    ) -> None:
        user_ids = {user_id}
        sub_id, duration = subscription

        await user_subscription_rep.bulk_subscribe_free(
            user_ids=user_ids, free_sub_id=sub_id, duration=timedelta(days=duration)
        )

        user_sub = await user_subscription_rep.get_active(user_id=user_id)
        assert user_sub.subscription_id == sub_id
        assert user_sub.is_active is True
