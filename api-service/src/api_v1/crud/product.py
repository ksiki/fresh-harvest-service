from api_v1.utils.converter import (
    products_to_products_response,
)
from schemas.product import ProductResponse

from shared.db.rep_container import RepContainer, with_repositories


@with_repositories
async def get_all_products(repositories: RepContainer) -> list[ProductResponse]:
    products = await repositories.product_rep.get_all_entities()
    return await products_to_products_response(
        img_rep=repositories.img_rep, products=products
    )
