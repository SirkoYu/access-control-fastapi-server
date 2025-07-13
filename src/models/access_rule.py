from datetime import time

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import Base
from .mixins import IntIdPkMixin

class AccessRule(Base, IntIdPkMixin):
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    time_from: Mapped[time]
    time_to: Mapped[time]

    __table_args__ = (
        UniqueConstraint("room_id", "role_id"),
    )