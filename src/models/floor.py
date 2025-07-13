from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .building import Building
    from .room import Room


class Floor(Base, IntIdPkMixin):
    floor_number: Mapped[int]
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["Building"] = relationship(back_populates="floors")
    rooms: Mapped[list["Room"]] = relationship(back_populates="floor")