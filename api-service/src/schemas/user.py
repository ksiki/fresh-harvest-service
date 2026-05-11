from pydantic import BaseModel
from schemas.base import BaseResponse


class CreateUser(BaseModel):
    tg_id: int


class CreateUserResponse(BaseResponse):
    user_id: int
