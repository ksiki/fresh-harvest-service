from db.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    str_id: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(32))
    icon_name: Mapped[str] = mapped_column(String(255))
    icon_seeded: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    def __repr__(self) -> str:
        return (
            f"<Product str_id: {self.str_id}, {self.name}, seeded: {self.icon_seeded}>"
        )
