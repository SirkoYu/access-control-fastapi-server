from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from .base import Base
from .mixins import IntIdPkMixin

class Role(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(48), unique=True)
    description: Mapped[str] = mapped_column(Text)