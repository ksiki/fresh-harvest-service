from dependencies.tasks import (
    get_subscription_repository,
    get_user_subscription_repository,
)
from handlers.user_subscriptions import UserSubscriptionHandler
from taskiq_dependencies import Depends

from shared.enums.task import TaskType
from shared.queue.broker import broker


@broker.task(task_name=TaskType.CHECKING_USER_SUBSCRIPTIONS)
async def checking_user_subscriptions_task(
    user_subs_rep=Depends(get_user_subscription_repository),
    sub_rep=Depends(get_subscription_repository),
):
    await UserSubscriptionHandler.renew_expired_subscriptions_with_free(
        user_subs_rep=user_subs_rep,
        sub_rep=sub_rep,
    )
