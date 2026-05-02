from datetime import datetime

from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    tg_id: Mapped[int] = mapped_column(unique=True)
    first_activity: Mapped[datetime]
    last_activity: Mapped[datetime]

    def __repr__(self) -> str:
        return f"<User {self.tg_id}, first_activity: {self.first_activity}, last_activity: {self.last_activity}>"
