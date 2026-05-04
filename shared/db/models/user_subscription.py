from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

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

    def __repr__(self) -> str:
        return f"<UserSubscription user_id: {self.title}, sub_id: {self.subscription_id}, purchase_at: {self.purchase_at}, expires_at: {self.expires_at}, is_active: {self.is_active}>"
