from functools import wraps
from typing import Callable

from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.db_s3 import database as s3_db
from shared.db.core.db_sql import database as sql_db
from shared.db.repositories.images import ImageRepository
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.products import ProductRepository
from shared.db.repositories.subscriptions import SubscriptionRepository
from shared.db.repositories.user_subscriptions import UserSubscriptionRepository
from shared.db.repositories.users import UserRepository


class RepContainer:
    def __init__(self, sql_session: AsyncSession, s3_session: AioBaseClient):
        self.sql = sql_session
        self.s3 = s3_session

    @property
    def img_rep(self) -> ImageRepository:
        return ImageRepository(session=self.s3)

    @property
    def post_rep(self) -> PostRepository:
        return PostRepository(session=self.sql)

    @property
    def user_rep(self) -> UserRepository:
        return UserRepository(session=self.sql)

    @property
    def sub_rep(self) -> SubscriptionRepository:
        return SubscriptionRepository(session=self.sql)

    @property
    def user_sub_rep(self) -> UserSubscriptionRepository:
        return UserSubscriptionRepository(session=self.sql)

    @property
    def product_rep(self) -> ProductRepository:
        return ProductRepository(session=self.sql)


def with_repositories(func) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Callable:
        async with sql_db.session_scope() as sql, s3_db.session_scope() as s3:
            return await func(
                *args,
                repositories=RepContainer(sql_session=sql, s3_session=s3),
                **kwargs,
            )

    return wrapper
