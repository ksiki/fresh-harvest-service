import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from shared.db.models.base import BaseModel
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.products import ProductRepository
from shared.db.repositories.subscriptions import SubscriptionRepository
from shared.db.repositories.user_subscriptions import UserSubscriptionRepository
from shared.db.repositories.users import UserRepository


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    with PostgresContainer("postgis/postgis:15-3.3-alpine") as postgres:
        yield postgres


@pytest_asyncio.fixture(scope="function")
async def engine(postgres_container) -> AsyncEngine:
    url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        await conn.execute(text("create schema if not exists content"))
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncSession:
    connection = await engine.connect()
    trans = await connection.begin()

    Session = async_sessionmaker(bind=connection, expire_on_commit=False)
    async with Session() as session:
        yield session

    await trans.rollback()
    await connection.close()


@pytest_asyncio.fixture
def post_rep(session) -> PostRepository:
    return PostRepository(session=session)


@pytest_asyncio.fixture
def product_rep(session) -> ProductRepository:
    return ProductRepository(session=session)


@pytest_asyncio.fixture
def user_rep(session) -> UserRepository:
    return UserRepository(session=session)


@pytest_asyncio.fixture
def subscription_rep(session) -> SubscriptionRepository:
    return SubscriptionRepository(session=session)


@pytest_asyncio.fixture
def user_subscription_rep(session) -> UserSubscriptionRepository:
    return UserSubscriptionRepository(session=session)


@pytest_asyncio.fixture
async def user_id(user_rep: UserRepository) -> int:
    user_id = await user_rep.register(tg_id=12345)
    return user_id
