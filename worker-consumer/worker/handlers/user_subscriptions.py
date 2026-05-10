import logging
from datetime import timedelta

from shared.db.repositories.subscriptions import SubscriptionRepository
from shared.db.repositories.user_subscriptions import UserSubscriptionRepository

logger = logging.getLogger(__name__)


class UserSubscriptionHandler:
    @staticmethod
    async def renew_expired_subscriptions_with_free(
        user_subs_rep: UserSubscriptionRepository, sub_rep: SubscriptionRepository
    ) -> None:
        expired_user_ids = await user_subs_rep.deactivate_expired_subscriptions()

        if len(expired_user_ids) == 0:
            logger.info("No expired subscriptions found.")
            return

        free_sub = await sub_rep.get_free_subscription()

        await user_subs_rep.bulk_subscribe_free(
            expired_user_ids, free_sub.id, timedelta(free_sub.duration_days)
        )
