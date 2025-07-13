from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .room import Room
    from .role import Role


class AccessRule(Base, IntIdPkMixin):
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    time_from: Mapped[time]
    time_to: Mapped[time]

    __table_args__ = (
        UniqueConstraint("room_id", "role_id"),
    )

    room: Mapped["Room"] = relationship(back_populates="access_rules")
    role: Mapped["Role"] = relationship(back_populates="access_rules")