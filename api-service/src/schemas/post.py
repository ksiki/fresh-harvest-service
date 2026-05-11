from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from schemas.base import BaseResponse


class CreatePost(BaseModel):
    product_id: int
    description: str
    price: Decimal
    geo: str


class PostResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    image_url: str
    description: str
    price: Decimal
    geo: str
    pub_at: datetime
    disable_at: datetime
    delete_at: datetime
    status: str


class CreatePostResponse(BaseResponse):
    post_id: int


class GetPostsResponse(BaseResponse):
    posts: list[PostResponse]


class ActivatePostResponse(BaseResponse):
    pass


class ArchivatePostResponse(BaseResponse):
    pass
