from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin, TimestampMixin
from src.constants import Action

if TYPE_CHECKING:
    from .room import Room
    from .user import User


class AccessLog(Base, IntIdPkMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    action: Mapped[Action] = mapped_column(Enum(Action, name="action_enum"))
    access_allowed: Mapped[bool] = mapped_column(default=True, server_default="1")

    room: Mapped["Room"] = relationship(back_populates="access_logs")
    user: Mapped["User"] = relationship(back_populates="access_logs")