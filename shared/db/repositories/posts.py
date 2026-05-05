import datetime
import logging
from datetime import timedelta
from decimal import Decimal

from geoalchemy2.elements import WKBElement
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.common_config import constants
from shared.db.models.post import Post
from shared.db.repositories.base import BaseRepository
from shared.enums.post_status import PostStatus

logger = logging.getLogger(__name__)


class PostRepository(BaseRepository[Post, AsyncSession]):
    model = Post

    async def get_by_products(self, products: set[int]) -> list[Post]:
        stmt = select(Post).where(
            Post.product_id.in_(products), Post.status == PostStatus.ACTIVE
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user(self, user_id: int) -> list[Post]:
        stmt = select(Post).where(
            Post.user_id == user_id,
            Post.status.in_([PostStatus.ACTIVE, PostStatus.ARCHIVE]),
            Post.delete_at > func.now(),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def reactivate(self, post_id: int, lifetime: timedelta) -> None:
        await self._change_status(
            post_id=post_id,
            status=PostStatus.ACTIVE,
            disable_at=func.now() + lifetime,
            delete_at=func.now() + lifetime + constants.archive_lifetime,
        )

    async def archivate(self, post_id: int) -> None:
        await self._change_status(
            post_id=post_id,
            status=PostStatus.ARCHIVE,
            disable_at=func.now(),
            delete_at=func.now() + constants.archive_lifetime,
        )

    async def archivate_all_old_posts(self) -> None:
        stmt = (
            update(Post)
            .where(Post.status == PostStatus.ACTIVE, Post.disable_at < func.now())
            .values(status=PostStatus.ARCHIVE)
        )
        await self.session.execute(stmt)

    async def delete_all_old_posts(self) -> None:
        stmt = delete(Post).where(
            Post.status == PostStatus.ARCHIVE, Post.delete_at < func.now()
        )
        await self.session.execute(stmt)

    async def create(
        self,
        user_id: int,
        prod_id: int,
        img_name: str,
        description: str,
        price: Decimal,
        geo: WKBElement | str,
        lifetime: timedelta,
    ) -> int:
        logger.info("Create post")
        stmt = (
            insert(Post)
            .values(
                user_id=user_id,
                product_id=prod_id,
                image_name=img_name,
                description=description,
                price=price,
                geo=geo,
                pub_at=func.now(),
                disable_at=func.now() + lifetime,
                delete_at=func.now() + lifetime + constants.archive_lifetime,
                status=PostStatus.VALIDATE,
            )
            .returning(Post.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def _change_status(
        self,
        post_id: int,
        status: PostStatus,
        disable_at: datetime,
        delete_at: datetime,
    ) -> None:
        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(status=status, disable_at=disable_at, delete_at=delete_at)
        )
        await self.session.execute(stmt)
