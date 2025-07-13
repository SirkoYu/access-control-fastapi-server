from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from .base import Base
from .mixins import IntIdPkMixin

class Room(Base, IntIdPkMixin):
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id"))
    name: Mapped[str] = mapped_column(String(48))