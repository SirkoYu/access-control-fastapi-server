from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base
from .mixins import IntIdPkMixin, TimestampMixin

if TYPE_CHECKING:
    from .room import Room
    from .user import User


class CurrentPresence(Base, IntIdPkMixin, TimestampMixin):
    __tablename__ = "current_presence" # type: ignore

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    room: Mapped["Room"] = relationship(back_populates="current_presence")
    user: Mapped["User"] = relationship(back_populates="current_presence")