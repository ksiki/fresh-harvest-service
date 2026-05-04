from datetime import datetime
from decimal import Decimal

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from shared.common_config import settings
from shared.db.models.base import BaseModel
from shared.db.models.product import Product
from shared.db.models.user import User
from shared.enums.post_status import PostStatus


class Post(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id))
    image_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    geo: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False)
    )
    pub_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    disable_at: Mapped[datetime]
    delete_at: Mapped[datetime]
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, schema=settings.database_schema)
    )

    __table_args__ = (
        Index("idx_post_geo_gist", "geo", postgresql_using="gist"),
        CheckConstraint("price >= 0", name="post_check_price_positive"),
        {"schema": settings.database_schema},
    )

    def __repr__(self) -> str:
        return f"<Post user_id={self.user_id}, product_id={self.product_id}, price={self.price}, pub_at={self.pub_at}, disable_at={self.disable_at}, status={self.status}>"
