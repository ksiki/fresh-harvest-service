from fastapi import Depends, HTTPException, status

from shared.db.core.db_s3 import database as s3_db
from shared.db.core.db_sql import database as sql_db
from shared.db.models.subscription import Subscription
from shared.db.rep_container import RepContainer, with_repositories
from shared.enums.post_status import PostStatus


async def get_repositories() -> RepContainer:
    async with sql_db.session_scope() as sql, s3_db.session_scope() as s3:
        yield RepContainer(sql_session=sql, s3_session=s3)


async def user_data(
    tg_id: int, repositories: RepContainer = Depends(get_repositories)
) -> tuple:
    user_id = await repositories.user_rep.get_id_by_tg_id(tg_id=tg_id)
    user_sub_data = await repositories.user_sub_rep.get_active(user_id=user_id)
    sub_data = await repositories.sub_rep.get_by_id(id=user_sub_data.subscription_id)

    return (user_id, sub_data)


async def check_user_and_update_activity(
    tg_id: int, repositories: RepContainer = Depends(get_repositories)
) -> int:
    user_id = await repositories.user_rep.get_id_by_tg_id(tg_id=tg_id)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not registered"
        )

    await repositories.user_rep.update_last_activity(user_id=user_id)
    return user_id


@with_repositories
async def check_active_posts_limit(
    user_id: int,
    sub_data: Subscription,
    repositories: RepContainer = None,
) -> None:
    all_posts = await repositories.post_rep.get_by_user(user_id=user_id)
    active_posts = [post for post in all_posts if post.status == PostStatus.ACTIVE]
    if len(active_posts) >= sub_data.active_post_limit:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The limit of active posts has been exceeded.",
        )
