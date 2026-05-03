from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.common_config import settings
from shared.db.models.base import Base


class Subscription(Base):
    str_id: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(String(100))
    active_post_limit: Mapped[int]
    post_lifetime_hours: Mapped[int]
    duration_days: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    __table_args__ = (
        CheckConstraint("price >= 0", name="subscription_check_price_positive"),
        CheckConstraint(
            "post_limit > 0", name="subscription_check_post_limit_positive"
        ),
        CheckConstraint(
            "duration_days > 0", name="subscription_check_duration_days_positive"
        ),
        {"schema": settings.database_schema},
    )

    def __repr__(self) -> str:
        return f"<Subscription str_id: {self.str_id}, {self.title} ({self.price} USD)>"
