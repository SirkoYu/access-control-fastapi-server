from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .base import Base
from .mixins import IntIdPkMixin

class Floor(Base, IntIdPkMixin):
    floor_number: Mapped[int]
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))