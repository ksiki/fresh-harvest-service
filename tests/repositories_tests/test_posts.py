from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models.post import Post
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.products import ProductRepository
from shared.db.repositories.users import UserRepository
from shared.enums.post_status import PostStatus


@pytest_asyncio.fixture
async def product_id(product_rep: ProductRepository) -> int:
    await product_rep.create_or_update(
        str_id="apple", name="Apple", icon_name="apple.png", is_active=True
    )
    product = await product_rep.get_by_str_id("apple")
    return product.id


@pytest_asyncio.fixture
def post_factory(
    post_rep: PostRepository,
    user_rep: UserRepository,
    product_rep: ProductRepository,
) -> Callable:
    async def _create_post(
        tg_id: int = 12345,
        prod_str_id: str = "apple",
        status=PostStatus.VALIDATE,
        disable_at: datetime = func.now(),
        delete_at: datetime = func.now() + timedelta(hours=24),
    ) -> int:
        user_id = await user_rep.get_id_by_tg_id(tg_id)
        if not user_id:
            user_id = await user_rep.register(tg_id)

        await product_rep.create_or_update(
            str_id=prod_str_id,
            name=prod_str_id.capitalize(),
            icon_name=f"{prod_str_id}.png",
            is_active=True,
        )
        product = await product_rep.get_by_str_id(prod_str_id)

        params = {
            "user_id": user_id,
            "prod_id": product.id,
            "img_name": "post.jpg",
            "description": "Description",
            "price": Decimal("10"),
            "geo": "POINT(0 0)",
            "lifetime": timedelta(hours=24),
        }

        post_id = await post_rep.create(**params)

        if status != PostStatus.VALIDATE:
            await post_rep._change_status(
                post_id, status=status, disable_at=disable_at, delete_at=delete_at
            )

        return post_id

    return _create_post


@pytest.mark.asyncio
class TestPostRep:
    async def test_create_post(
        self, post_rep: PostRepository, user_id: int, product_id: int
    ) -> None:
        post_id = await post_rep.create(
            user_id=user_id,
            prod_id=product_id,
            img_name="post.png",
            description="post description",
            price=0.99,
            geo="POINT(24.3 25.3)",
            lifetime=timedelta(hours=24),
        )

        post = await post_rep.get_by_id(id=post_id)

        assert post.id == post_id
        assert post.status == PostStatus.VALIDATE

    async def test_get_by_products(
        self, post_factory: Callable, post_rep: PostRepository
    ):
        post_id_1 = await post_factory(
            tg_id=1, prod_str_id="apple", status=PostStatus.ACTIVE
        )
        await post_factory(tg_id=2, prod_str_id="banana", status=PostStatus.ACTIVE)

        apple_posts = await post_rep.get_by_products({1})

        assert len(apple_posts) == 1
        assert apple_posts[0].id == post_id_1

    async def test_get_by_user(
        self, post_factory: Callable, post_rep: PostRepository, user_rep: UserRepository
    ):
        post_id_1 = await post_factory(
            tg_id=1, prod_str_id="apple", status=PostStatus.ACTIVE
        )
        await post_factory(tg_id=2, prod_str_id="banana", status=PostStatus.ACTIVE)

        user_id = await user_rep.get_id_by_tg_id(tg_id=1)
        user_posts = await post_rep.get_by_user(user_id=user_id)

        assert len(user_posts) == 1
        assert user_posts[0].id == post_id_1

    async def test_archivate_all_old_posts(
        self, post_factory: Callable, post_rep: PostRepository, session: AsyncSession
    ):
        post_id = await post_factory(
            tg_id=1,
            prod_str_id="apple",
            status=PostStatus.ACTIVE,
            disable_at=func.now() - timedelta(hours=1),
        )
        await post_factory(tg_id=2, prod_str_id="banana", status=PostStatus.ACTIVE)
        await post_factory(tg_id=3, prod_str_id="orange", status=PostStatus.VALIDATE)

        await post_rep.archivate_all_old_posts()

        stmt = select(Post).where(Post.status == PostStatus.ARCHIVE)
        result = await session.execute(stmt)
        archive_posts = list(result.scalars().all())

        assert len(archive_posts) == 1
        assert archive_posts[0].id == post_id

    async def test_delete_all_old_posts(
        self, post_factory: Callable, post_rep: PostRepository, session: AsyncSession
    ):
        archive_post_id = await post_factory(
            tg_id=1, prod_str_id="apple", status=PostStatus.ARCHIVE
        )
        await post_factory(
            tg_id=2,
            prod_str_id="watermalon",
            status=PostStatus.ARCHIVE,
            delete_at=func.now() - timedelta(hours=1),
        )
        await post_factory(tg_id=3, prod_str_id="banana", status=PostStatus.ACTIVE)
        await post_factory(tg_id=4, prod_str_id="orange", status=PostStatus.VALIDATE)

        await post_rep.delete_all_old_posts()

        base_stmp = select(Post)
        result = await session.execute(base_stmp)
        all_posts = list(result.scalars().all())

        assert len(all_posts) == 3

        archive_stmt = base_stmp.where(Post.status == PostStatus.ARCHIVE)
        result = await session.execute(archive_stmt)
        archive_posts = list(result.scalars().all())

        assert len(archive_posts) == 1
        assert archive_posts[0].id == archive_post_id
