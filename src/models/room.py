from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from floor import Floor
    from access_log import AccessLog
    from access_rule import AccessRule
    from current_presence import CurrentPresence


class Room(Base, IntIdPkMixin):
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id"))
    name: Mapped[str] = mapped_column(String(48))

    floor: Mapped["Floor"] = relationship(back_populates="rooms")
    access_logs: Mapped[list["AccessLog"]] = relationship(back_populates="room")
    access_rules: Mapped[list["AccessRule"]] = relationship(back_populates="room")
    current_presence: Mapped[list["CurrentPresence"]] = relationship(back_populates="room")