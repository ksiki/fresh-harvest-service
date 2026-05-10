from shared.enums.task import TaskType
from shared.queue.broker import broker


@broker.task(
    task_name=TaskType.ARCHIVE_POSTS,
    schedule=[{"cron": "0 */2 * * *"}],
)
async def archive_posts_task() -> None:
    from worker.tasks.posts import archive_posts_task

    await archive_posts_task()


@broker.task(
    task_name=TaskType.DELETE_POSTS,
    schedule=[{"cron": "40 */2 * * *"}],
)
async def delete_posts_task() -> None:
    from worker.tasks.posts import delete_posts_task

    await delete_posts_task()


@broker.task(
    task_name=TaskType.CHECKING_USER_SUBSCRIPTIONS,
    schedule=[{"cron": "* 0 * * *"}],
)
async def checking_user_subscriptions_task() -> None:
    from worker.tasks.users import checking_user_subscriptions_task

    await checking_user_subscriptions_task()


@broker.task(task_name=TaskType.VALIDATE_POST)
async def validate_post_task(post_id: int) -> None:
    from worker.tasks.posts import validate_post_task

    await validate_post_task(post_id=post_id)


@broker.task(task_name=TaskType.NOTIFY_USER)
async def notify_user(tg_id: int, message: str) -> None:
    from bot.task_handler import send_notify

    await send_notify(tg_id=tg_id, message=message)
