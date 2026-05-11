from typing import Final

from api_v1.core.config import constants
from api_v1.core.dependencies import check_user_and_update_activity
from api_v1.endpoints.post import router as post_router
from api_v1.endpoints.product import router as product_router
from api_v1.endpoints.subscription import router as subscription_router
from api_v1.endpoints.user import router as user_router
from api_v1.endpoints.user_subscription import router as user_subscription_router
from fastapi import APIRouter, Depends

api_router: Final[APIRouter] = APIRouter(prefix=constants.prefix)

api_router.include_router(router=user_router, prefix="/user")
api_router.include_router(
    post_router, prefix="/post", dependencies=[Depends(check_user_and_update_activity)]
)
api_router.include_router(
    product_router,
    prefix="/product",
    dependencies=[Depends(check_user_and_update_activity)],
)
api_router.include_router(
    subscription_router,
    prefix="/subscription-data",
    dependencies=[Depends(check_user_and_update_activity)],
)
api_router.include_router(
    user_subscription_router,
    prefix="/subscription-service",
    dependencies=[Depends(check_user_and_update_activity)],
)
