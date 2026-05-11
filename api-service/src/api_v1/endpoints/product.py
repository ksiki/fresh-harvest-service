from typing import Final

import api_v1.crud.product as crud
from fastapi import APIRouter, status
from schemas.product import GetProductsResponse

router: Final[APIRouter] = APIRouter()


@router.get("/", response_model=GetProductsResponse, status_code=status.HTTP_200_OK)
async def get_all_products() -> GetProductsResponse:
    products = await crud.get_all_products()
    return GetProductsResponse(products=products)
