from datetime import time

from pydantic import BaseModel

from .general_schemas import (
    Room, 
    Role,
)


class AccessRuleBase(BaseModel):
    room_id: int
    role_id: int
    time_from: time
    time_to: time

class AccessRuleCreate(AccessRuleBase):
    pass

class AccessRuleUpdate(AccessRuleBase):
    pass

class AccessRuleUpdatePartical(BaseModel):
    room_id: int|None = None
    role_id: int| None = None
    time_from: time| None = None
    time_to: time| None = None

class AccessRuleOut(AccessRuleBase):
    id: int

class AccessRuleWithRoom(AccessRuleOut):
    room: Room

class AccessRuleWithRole(AccessRuleOut):
    role: Role