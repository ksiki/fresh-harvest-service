from schemas.post import PostResponse
from schemas.product import ProductResponse
from schemas.subscription import SubscriptionResponse

from shared.db.models.post import Post
from shared.db.models.product import Product
from shared.db.models.subscription import Subscription
from shared.db.repositories.images import ImageRepository
from shared.enums.image_category import ImageCategory


async def posts_to_posts_response(
    img_rep: ImageRepository, posts: list[Post]
) -> list[PostResponse]:
    result = [
        PostResponse(
            id=post.id,
            user_id=post.user_id,
            product_id=post.product_id,
            image_url=await img_rep.get_url(
                category=ImageCategory.POST, name=post.image_name
            ),
            description=post.description,
            price=post.price,
            geo=str(post.geo),
            pub_at=post.pub_at,
            disable_at=post.disable_at,
            delete_at=post.delete_at,
            status=str(post.status),
        )
        for post in posts
    ]
    return result


async def products_to_products_response(
    img_rep: ImageRepository, products: list[Product]
) -> list[ProductResponse]:
    result = [
        ProductResponse(
            str_id=product.str_id,
            name=product.name,
            image_url=await img_rep.get_url(
                category=ImageCategory.PRODUCT, name=product.icon_name
            ),
        )
        for product in products
    ]
    return result


async def subscriptions_to_subscriptions_response(
    subscriptions: list[Subscription],
) -> list[SubscriptionResponse]:
    result = [
        SubscriptionResponse(
            str_id=sub.str_id,
            title=sub.title,
            active_post_limit=sub.active_post_limit,
            post_lifetime_hours=sub.post_lifetime_hours,
            duration_days=sub.duration_days,
            price=sub.price,
        )
        for sub in subscriptions
    ]
    return result
