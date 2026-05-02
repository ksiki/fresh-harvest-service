from datetime import datetime

from db.models.base import Base
from db.models.subscription import Subscription
from db.models.user import User
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class UserSubscription(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    subscription_id: Mapped[int] = mapped_column(ForeignKey(Subscription.id))
    purchase_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    expires_at: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    def __repr__(self) -> str:
        return f"<UserSubscription user_id: {self.title}, sub_id: {self.subscription_id}, purchase_at: {self.purchase_at}, expires_at: {self.expires_at}, is_active: {self.is_active}>"
