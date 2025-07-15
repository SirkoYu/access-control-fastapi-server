from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role import Role
    from .access_log import AccessLog
    from .current_presence import CurrentPresence


class User(Base, IntIdPkMixin):
    first: Mapped[str] = mapped_column(String(32))
    last: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="1")
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")

    roles: Mapped[list["Role"]] = relationship(secondary="user_role_association", back_populates="users") # type: ignore
    access_logs: Mapped[list["AccessLog"]] = relationship(back_populates="user")
    current_presence: Mapped["CurrentPresence"] = relationship(back_populates="user")