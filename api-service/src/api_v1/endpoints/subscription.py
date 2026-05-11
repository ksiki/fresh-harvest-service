from typing import Final

import api_v1.crud.subscription as crud
from fastapi import APIRouter, status
from schemas.subscription import GetSubscriptionsResponse

router: Final[APIRouter] = APIRouter()


@router.get(
    "/", response_model=GetSubscriptionsResponse, status_code=status.HTTP_200_OK
)
async def get_all_subscriptions() -> GetSubscriptionsResponse:
    subscriptions = await crud.get_all_subscriptions()
    return GetSubscriptionsResponse(subscriptions=subscriptions)
