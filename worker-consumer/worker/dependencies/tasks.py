from contextlib import asynccontextmanager

from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq_dependencies import Depends

from shared.db.core.db_s3 import database as s3_db
from shared.db.core.db_sql import database as sql_db
from shared.db.repositories.images import ImageRepository
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.subscriptions import SubscriptionRepository
from shared.db.repositories.user_subscriptions import UserSubscriptionRepository
from shared.db.repositories.users import UserRepository


@asynccontextmanager
async def _get_sql_session() -> AsyncSession:
    async with sql_db.session_dependency() as session:
        yield session


@asynccontextmanager
async def _get_s3_session() -> AioBaseClient:
    async with s3_db.session_dependency() as session:
        yield session


def get_image_repository(
    session: AioBaseClient = Depends(_get_s3_session),
) -> ImageRepository:
    return ImageRepository(session=session)


def get_post_repository(
    session: AsyncSession = Depends(_get_sql_session),
) -> PostRepository:
    return PostRepository(session=session)


def get_user_repository(
    session: AsyncSession = Depends(_get_sql_session),
) -> UserRepository:
    return UserRepository(session=session)


def get_subscription_repository(
    session: AsyncSession = Depends(_get_sql_session),
) -> SubscriptionRepository:
    return SubscriptionRepository(session=session)


def get_user_subscription_repository(
    session: AsyncSession = Depends(_get_sql_session),
) -> UserSubscriptionRepository:
    return UserSubscriptionRepository(session=session)
