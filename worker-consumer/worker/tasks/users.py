from worker.dependencies import RepContainer, with_repositories
from worker.handlers.user_subscriptions import UserSubscriptionHandler


@with_repositories
async def checking_user_subscriptions_task(repositories: RepContainer) -> None:
    await UserSubscriptionHandler.renew_expired_subscriptions_with_free(
        user_subs_rep=repositories.user_sub_rep,
        sub_rep=repositories.sub_rep,
    )
