import uuid
from datetime import timedelta

from api_v1.utils.post_halper import (
    posts_to_posts_response,
)
from schemas.post import CreatePost, PostResponse

from shared.db.models.subscription import Subscription
from shared.db.rep_container import RepContainer, with_repositories
from shared.enums.image_category import ImageCategory
from shared.queue.tasks import validate_post_task


@with_repositories
async def create_new_post(
    user_id: int,
    sub_data: Subscription,
    image: bytes,
    extension: str,
    post_data: CreatePost,
    repositories: RepContainer,
) -> int:
    post_rep = repositories.post_rep
    img_rep = repositories.img_rep

    img_name = f"{uuid.uuid4()}{extension}"
    post_id = await post_rep.create(
        user_id=user_id,
        image_name=img_name,
        **post_data.model_dump(),
        lifetime=timedelta(hours=sub_data.post_lifetime_hours),
    )
    await img_rep.upload(category=ImageCategory.POST, name=img_name, content=image)
    await validate_post_task.kiq(post_id=post_id)

    return post_id


@with_repositories
async def get_posts_by_user(
    user_id: int,
    repositories: RepContainer,
) -> list[PostResponse]:
    posts = await repositories.post_rep.get_by_user(user_id=user_id)
    return await posts_to_posts_response(img_rep=repositories.img_rep, posts=posts)


@with_repositories
async def get_posts_by_products(
    products: list[str],
    repositories: RepContainer,
) -> list[PostResponse]:
    posts = await repositories.post_rep.get_by_products(products=set(products))
    return await posts_to_posts_response(img_rep=repositories.img_rep, posts=posts)


@with_repositories
async def activate_post(
    post_id: int,
    sub_data: Subscription,
    repositories: RepContainer,
) -> None:
    await repositories.post_rep.reactivate(post_id=post_id, lifetime=timedelta())


@with_repositories
async def archivate_post(
    post_id: int,
    repositories: RepContainer,
) -> None:
    await repositories.post_rep.archivate(post_id=post_id)
