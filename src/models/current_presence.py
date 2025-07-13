from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .base import Base
from .mixins import IntIdPkMixin, TimestampMixin

class CurrentPresence(Base, IntIdPkMixin, TimestampMixin):
    __tablename__ = "current_presence" # type: ignore

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))