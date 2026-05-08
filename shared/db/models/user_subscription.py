from datetime import datetime

from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from shared.common_config import settings
from shared.db.models.base import BaseModel
from shared.db.models.subscription import Subscription
from shared.db.models.user import User


class UserSubscription(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    subscription_id: Mapped[int] = mapped_column(ForeignKey(Subscription.id))
    purchase_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    expires_at: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    __table_args__ = (
        Index(
            "idx_user_sub_active_uid", "user_id", postgresql_where=(is_active == True)
        ),
        Index(
            "idx_user_sub_expires_active",
            "expires_at",
            postgresql_where=(is_active == True),
        ),
        {"schema": settings.database_schema},
    )

    def __repr__(self) -> str:
        return f"<UserSubscription user_id: {self.title}, sub_id: {self.subscription_id}, purchase_at: {self.purchase_at}, expires_at: {self.expires_at}, is_active: {self.is_active}>"
