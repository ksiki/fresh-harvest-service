from decimal import Decimal

from pydantic import BaseModel
from schemas.base import BaseResponse


class SubscriptionResponse(BaseModel):
    id: int
    str_id: str
    title: str
    active_post_limit: int
    post_lifetime_hours: int
    duration_days: int
    price: Decimal


class GetSubscriptionsResponse(BaseResponse):
    subscriptions: list[SubscriptionResponse]
