from datetime import timedelta

from shared.db.rep_container import RepContainer, with_repositories


@with_repositories
async def subscribe_user(
    user_id: int,
    sub_id: int,
    repositories: RepContainer,
) -> None:
    sub_data = await repositories.sub_rep.get_by_id(id=sub_id)
    await repositories.user_sub_rep.subscribe(
        user_id=user_id, sub_id=sub_id, duration=timedelta(days=sub_data.duration_days)
    )
