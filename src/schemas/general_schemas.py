from datetime import datetime, time
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr
from annotated_types import MaxLen, MinLen, Ge

from models.access_log import Action


class Role(BaseModel):
    name: Annotated[str, MaxLen(48)]
    description: str|None
    id: int

class Room(BaseModel):
    id: int
    floor_id: int
    name: Annotated[str, MaxLen(48), MinLen(3)]

class AccessLog(BaseModel):
    id: int
    user_id: int
    room_id: int
    action: Action
    access_allowed: bool
    timestamp: datetime

class CurrentPresence(BaseModel):
    id: int
    timestamp: datetime
    room_id: int
    user_id: int

class Floor(BaseModel):
    floor_number: Annotated[int, Ge(0)]
    building_id: int
    id: int

class Building(BaseModel):
    name: Annotated[str, MaxLen(48), MinLen(3)]
    description: str
    address: Annotated[str, MaxLen(64), MinLen(3)]
    id: int

class AccessRule(BaseModel):
    id: int
    room_id: int
    role_id: int
    time_from: time
    time_to: time

class User(BaseModel):
    id: int
    first: Annotated[str, MaxLen(32), MinLen(3)]
    last: Annotated[str, MaxLen(32), MinLen(3)]
    email: EmailStr
    is_active: bool = True