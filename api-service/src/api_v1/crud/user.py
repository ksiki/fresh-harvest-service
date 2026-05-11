from datetime import timedelta

from schemas.user import CreateUser

from shared.db.rep_container import RepContainer, with_repositories


@with_repositories
async def register_new_user(user_data: CreateUser, repositories: RepContainer) -> int:
    user_rep = repositories.user_rep
    user_id = await user_rep.register(tg_id=user_data.tg_id)

    sub_rep = repositories.sub_rep
    user_sub_rep = repositories.user_sub_rep

    free_sub = await sub_rep.get_free_subscription()
    await user_sub_rep.subscribe(
        user_id=user_id,
        sub_id=free_sub.id,
        duration=timedelta(days=free_sub.duration_days),
    )

    return user_id
