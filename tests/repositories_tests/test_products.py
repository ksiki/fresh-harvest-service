import pytest

from shared.db.repositories.products import ProductRepository


@pytest.mark.asyncio
class TestUserRep:
    async def test_create_new_product(self, product_rep: ProductRepository):
        prod_str_id = "product"
        prod_name = "Product"
        await product_rep.create_or_update(
            str_id=prod_str_id, name="Product", icon_name="product.png", is_active=True
        )

        product = await product_rep.get_by_str_id(str_id=prod_str_id)

        assert product.str_id == prod_str_id
        assert product.name == prod_name
        assert product.icon_seeded is False

        await product_rep.change_icon_seeded_status(prod_id=product.id, new_status=True)
        product_after_change_status = await product_rep.get_by_str_id(
            str_id=prod_str_id
        )

        assert product_after_change_status.icon_seeded is True
