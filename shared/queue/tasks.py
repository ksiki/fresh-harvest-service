import logging

from shared.enums.task import TaskType
from shared.queue.broker import broker

logger = logging.getLogger(__name__)


@broker.task(
    task_name=TaskType.ARCHIVE_POSTS,
    schedule=[{"cron": "0 */2 * * *"}],
)
async def archive_posts_task():
    pass


@broker.task(
    task_name=TaskType.DELETE_POSTS,
    schedule=[{"cron": "40 */2 * * *"}],
)
async def delete_posts_task():
    pass


@broker.task(
    task_name=TaskType.CHECKING_USER_SUBSCRIPTIONS,
    schedule=[{"cron": "20 1-23/2 * * *"}],
)
async def checking_user_subscriptions_task():
    pass


@broker.task(task_name=TaskType.VALIDATE_POST)
async def validate_post_task(post_id: int):
    pass
