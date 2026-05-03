import logging

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.base_rep import BaseRepository
from shared.db.mixins.active_filter_mixin import ActiveFilterMixin
from shared.db.mixins.str_id_mixin import StrIdMixin
from shared.db.models.product import Product

logger = logging.getLogger(__name__)


class ProductRepository(
    BaseRepository[Product, AsyncSession],
    StrIdMixin[Product],
    ActiveFilterMixin[Product],
):
    model = Product

    async def change_icon_seeded_status(self, prod_id: int, new_status: bool) -> None:
        logger.info("Change icon seeded status")
        stmt = (
            update(Product).where(Product.id == prod_id).values(icon_seeded=new_status)
        )
        await self.session.execute(stmt)

    async def create_or_update(
        self, str_id: str, name: str, icon_name: str, is_active: bool
    ) -> None:
        logger.info("Create or update product")

        icon_seeded = False
        product = await self.get_by_str_id(str_id=str_id)
        if product and product.icon_name == icon_name and product.icon_seeded:
            icon_seeded = True

        stmt = insert(Product).values(
            str_id=str_id,
            name=name,
            icon_name=icon_name,
            icon_seeded=icon_seeded,
            is_active=is_active,
        )
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=["str_id"],
            set_={
                "name": stmt.excluded.name,
                "icon_name": stmt.excluded.icon_name,
                "icon_seeded": stmt.excluded.icon_seeded,
                "is_active": stmt.excluded.is_active,
            },
        )
        await self.session.execute(upsert_stmt)
