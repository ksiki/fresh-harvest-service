from typing import Final

from pydantic_settings import BaseSettings


class Constants(BaseSettings):
    prefix: str


constants: Final[Constants] = Constants(prefix="/api/v1")
