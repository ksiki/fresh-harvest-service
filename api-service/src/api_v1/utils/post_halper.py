from schemas.post import PostResponse

from shared.db.models.post import Post
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
