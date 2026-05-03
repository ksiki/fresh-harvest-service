import json
import logging
from pathlib import Path
from typing import Final

from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.image_rep import ImageCategory, ImageRepository
from shared.db.product_rep import ProductRepository
from shared.db.subscription_rep import SubscriptionRepository

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent
    DATA_PATH: Final[Path] = BASE_DIR / "assets" / "data"
    SEED_ICONS_PATH: Final[Path] = BASE_DIR / "assets" / "seed_icons"

    def __init__(
        self,
        sub_rep: SubscriptionRepository,
        prod_rep: ProductRepository,
        img_rep: ImageRepository,
    ):
        self.sub_rep = sub_rep
        self.prod_rep = prod_rep
        self.img_rep = img_rep

    @classmethod
    async def run_bootstrap(
        cls, pg_session: AsyncSession, s3_session: AioBaseClient
    ) -> None:
        seeder = cls(
            sub_rep=SubscriptionRepository(pg_session),
            prod_rep=ProductRepository(pg_session),
            img_rep=ImageRepository(s3_session),
        )
        await seeder.run_all()
        logger.info("Database seeding completed successfully.")

    async def run_all(self) -> None:
        logger.info("Starting database seeding.")
        await self._upload_subscriptions()
        await self._upload_products()
        await self._seed_product_icons()

    async def _upload_subscriptions(self) -> None:
        path = self.DATA_PATH / "subscriptions.json"
        with open(path, "r", encoding="utf-8") as file:
            subs = json.load(file)
            for sub_data in subs:
                await self.sub_rep.create_or_update(**sub_data)
        logger.info("Subscriptions uploaded.")

    async def _upload_products(self) -> None:
        path = self.DATA_PATH / "products.json"
        with open(path, "r", encoding="utf-8") as file:
            products = json.load(file)
            for prod_data in products:
                await self.prod_rep.create_or_update(**prod_data)
        logger.info("Products uploaded.")

    async def _seed_product_icons(self) -> None:
        products = await self.prod_rep.get_all_entities(only_active=False)
        for product in products:
            if not product.is_active:
                await self.img_rep.delete(
                    category=ImageCategory.PRODUCT, name=product.icon_name
                )
                await self.prod_rep.change_icon_seeded_status(
                    prod_id=product.id, new_status=False
                )
                continue
            if product.icon_seeded:
                continue

            file_path = self.SEED_ICONS_PATH / product.icon_name
            if not file_path.exists():
                logger.warning(f"Icon {file_path} not found")
                continue

            content = file_path.read_bytes()
            await self.img_rep.upload(
                category=ImageCategory.PRODUCT,
                name=product.icon_name,
                content=content,
            )
            await self.prod_rep.change_icon_seeded_status(
                prod_id=product.id, new_status=True
            )
        logger.info("Product icons seeded.")
