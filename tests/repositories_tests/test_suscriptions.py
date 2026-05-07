from contextlib import nullcontext as does_not_raise
from decimal import Decimal
from typing import Any

import pytest

from shared.db.core.exceptions import SubscriptionNotFoundError
from shared.db.repositories.subscriptions import SubscriptionRepository


@pytest.mark.asyncio
class TestSubscriptionRep:
    async def test_create_new_subscription(
        self, subscription_rep: SubscriptionRepository
    ) -> None:
        sub_str_id = "subscription"
        sub_title = "Subscription"
        await subscription_rep.create_or_update(
            str_id=sub_str_id,
            title=sub_title,
            active_post_limit=3,
            post_lifetime_hours=24,
            duration_days=30,
            price=Decimal("0.99"),
            is_active=True,
        )

        sub = await subscription_rep.get_by_str_id(str_id=sub_str_id)

        assert sub.str_id == sub_str_id
        assert sub.title == sub_title

    @pytest.mark.parametrize(
        "sub_str_id, expectation",
        [
            ("free", does_not_raise()),
            ("sub_free", does_not_raise()),
            ("free_sub", does_not_raise()),
            ("it_free_sub", does_not_raise()),
            ("paid", pytest.raises(SubscriptionNotFoundError)),
        ],
    )
    async def test_get_free_subscription(
        self,
        sub_str_id: str,
        expectation: Any,
        subscription_rep: SubscriptionRepository,
    ) -> None:
        await subscription_rep.create_or_update(
            str_id=sub_str_id,
            title="Subscription",
            active_post_limit=3,
            post_lifetime_hours=24,
            duration_days=30,
            price=Decimal("0.99"),
            is_active=True,
        )

        with expectation:
            sub = await subscription_rep.get_free_subscription()
            assert sub.str_id == sub_str_id
