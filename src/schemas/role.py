from typing import Annotated

from pydantic import BaseModel
from annotated_types import MaxLen

from .general_schemas import (
    User, 
    AccessRule
)


class RoleBase(BaseModel):
    name: Annotated[str, MaxLen(48)]
    description: str|None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleUpdatePartical(BaseModel):
    name: Annotated[str|None, MaxLen(48)] = None
    description: str|None = None

class RoleOut(RoleBase):
    id: int

class RoleWithUsers(RoleOut):
    users: list[User]

class RoleWithAccessRules(RoleOut):
    access_rules: list[AccessRule]