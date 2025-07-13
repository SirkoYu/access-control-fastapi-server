from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel

from .general_schemas import (
    AccessLog,
    CurrentPresence,
    Floor,
    AccessRule,
)

class RoomBase(BaseModel):
    floor_id: int
    name: Annotated[str, MaxLen(48), MinLen(3)]

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomUpdatePartical(BaseModel):
    floor_id: int|None = None
    name: str|None = None

class RoomOut(RoomBase):
    id: int

class RoomWithFloor(RoomOut):
    floor: Floor

class RoomWithAccessLogs(RoomOut):
    access_logs: list[AccessLog]

class RoomWithAccessRules(RoomOut):
    access_rules: list[AccessRule]

class RoomWithCurrentPresence(RoomOut):
    current_presence: list[CurrentPresence]
