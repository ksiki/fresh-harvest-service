from api_v1.utils.converter import (
    subscriptions_to_subscriptions_response,
)
from schemas.subscription import SubscriptionResponse

from shared.db.rep_container import RepContainer, with_repositories


@with_repositories
async def get_all_subscriptions(
    repositories: RepContainer,
) -> list[SubscriptionResponse]:
    subscriptions = await repositories.sub_rep.get_all_entities()
    return await subscriptions_to_subscriptions_response(subscriptions=subscriptions)
