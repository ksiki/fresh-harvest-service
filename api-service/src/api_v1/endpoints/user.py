from typing import Final

import api_v1.crud.user as crud
from fastapi import APIRouter, status
from schemas.user import CreateUser, CreateUserResponse

router: Final[APIRouter] = APIRouter()


@router.post(
    "/register", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED
)
async def register_new_user(user_data: CreateUser) -> CreateUserResponse:
    user_id = await crud.register_new_user(user_data=user_data)
    return CreateUserResponse(user_id=user_id)
