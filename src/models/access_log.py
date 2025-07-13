import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin, TimestampMixin

class Action(enum.StrEnum):
    enter = "Enter"
    exit = "Exit"

class AccessLog(Base, IntIdPkMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    action: Mapped[Action] = mapped_column(Enum(Action, name="action_enum"))
    access_allowed: Mapped[bool] = mapped_column(default=True, server_default="1")
