from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .floor import Floor


class Building(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(48), unique=True)
    description: Mapped[str|None] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String(64), unique=True)

    floors: Mapped[list["Floor"]] = relationship(back_populates="building")