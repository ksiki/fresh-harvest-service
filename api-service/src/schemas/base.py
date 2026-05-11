from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    status: str = "ok"

    model_config = ConfigDict(from_attributes=True)
