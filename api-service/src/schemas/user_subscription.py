from pydantic import BaseModel
from schemas.base import BaseResponse


class UserSubscriptionResponse(BaseResponse):
    pass


class UserSubscribe(BaseModel):
    tg_id: int
    subscribtion_id: int
