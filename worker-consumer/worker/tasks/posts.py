from dependencies.tasks import (
    get_image_repository,
    get_post_repository,
    get_user_repository,
)
from handlers.posts import PostHandler
from taskiq_dependencies import Depends

from shared.db.repositories.images import ImageRepository
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.users import UserRepository
from shared.enums.task import TaskType
from shared.queue.broker import broker


@broker.task(task_name=TaskType.ARCHIVE_POSTS)
async def archive_posts_task(post_rep: PostRepository = Depends(get_post_repository)):
    await PostHandler.archive_posts(post_rep=post_rep)


@broker.task(task_name=TaskType.DELETE_POSTS)
async def delete_posts_task(
    post_rep: PostRepository = Depends(get_post_repository),
    img_rep: ImageRepository = Depends(get_image_repository),
):
    await PostHandler.delete_posts(post_rep=post_rep, img_rep=img_rep)


@broker.task(task_name=TaskType.VALIDATE_POST)
async def validate_post_task(
    post_id: int,
    post_rep: PostRepository = Depends(get_post_repository),
    user_rep: UserRepository = Depends(get_user_repository),
    image_rep: ImageRepository = Depends(get_image_repository),
):
    await PostHandler.validate_posts(
        post_id=post_id,
        post_rep=post_rep,
        user_rep=user_rep,
        image_rep=image_rep,
    )
