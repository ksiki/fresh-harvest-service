from worker.dependencies import RepContainer, with_repositories
from worker.handlers.posts import PostHandler


@with_repositories
async def archive_posts_task(repositories: RepContainer):
    await PostHandler.archive_posts(post_rep=repositories.post_rep)


@with_repositories
async def delete_posts_task(repositories: RepContainer):
    await PostHandler.delete_posts(
        post_rep=repositories.post_rep,
        img_rep=repositories.img_rep,
    )


@with_repositories
async def validate_post_task(post_id: int, repositories: RepContainer):
    await PostHandler.validate_posts(
        post_id=post_id,
        post_rep=repositories.post_rep,
        user_rep=repositories.user_rep,
        image_rep=repositories.img_rep,
    )
