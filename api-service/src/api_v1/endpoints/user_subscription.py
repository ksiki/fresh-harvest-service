from typing import Final

import api_v1.crud.user_subscription as crud
from api_v1.core.dependencies import user_data
from fastapi import APIRouter, Depends, status
from schemas.user_subscription import (
    UserSubscribe,
    UserSubscriptionResponse,
)

router: Final[APIRouter] = APIRouter()


@router.post(
    "/subscribe",
    response_model=UserSubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_post(
    sub_data: UserSubscribe = Depends(),
    user_data: tuple = Depends(user_data),
) -> UserSubscriptionResponse:
    user_id, _ = user_data
    await crud.subscribe_user(user_id=user_id, sub_id=sub_data.subscribtion_id)
    return UserSubscriptionResponse()
