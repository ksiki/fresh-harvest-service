import re

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from shared.common_config import settings


class BaseModel(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"schema": settings.database_schema}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
