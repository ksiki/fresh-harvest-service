from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from shared.db.models.base import Base


class User(Base):
    tg_id: Mapped[int] = mapped_column(unique=True)
    first_activity: Mapped[datetime]
    last_activity: Mapped[datetime]

    def __repr__(self) -> str:
        return f"<User {self.tg_id}, first_activity: {self.first_activity}, last_activity: {self.last_activity}>"
