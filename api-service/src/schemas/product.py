from pydantic import BaseModel
from schemas.base import BaseResponse


class ProductResponse(BaseModel):
    str_id: str
    name: str
    image_url: str


class GetProductsResponse(BaseResponse):
    products: list[ProductResponse]
