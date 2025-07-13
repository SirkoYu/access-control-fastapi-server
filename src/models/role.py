from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .access_rule import AccessRule
    from .user import User


class Role(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(48), unique=True)
    description: Mapped[str] = mapped_column(Text)

    access_rules: Mapped[list["AccessRule"]] = relationship(back_populates="role")
    users: Mapped[list["User"]] = relationship(secondary="user_role_association", back_populates="roles")  # type: ignore