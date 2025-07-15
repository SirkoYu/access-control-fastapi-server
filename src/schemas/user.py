from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr

from .general_schemas import (
    Role,
    AccessLog,
    CurrentPresence,
)


str_max32_min3 = Annotated[str, MaxLen(32), MinLen(3)]


class UserBase(BaseModel):
    first: str_max32_min3
    last: str_max32_min3
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    password: Annotated[str, MaxLen(64)]

class UserUpdate(UserCreate):
    pass

class UserUpdatePatrical(BaseModel):
    first: str_max32_min3 | None = None
    last: str_max32_min3 | None = None
    email: EmailStr | None = None
    password: Annotated[str| None, MaxLen(64)] = None
    is_admin: bool|None = None
    is_active: bool|None = None
    
class UserOut(UserBase):
    id: int

class UserWithRoles(UserOut):
    roles: list[Role]

class UserWithAccessLogs(UserOut):
    access_logs: list[AccessLog]

class UserWithCurrentPresence(UserOut):
    current_presence: CurrentPresence