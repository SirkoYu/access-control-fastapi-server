from datetime import datetime

from pydantic import BaseModel

from models.access_log import Action
from .general_schemas import User, Room

class AccessLogBase(BaseModel):
    user_id: int
    room_id: int
    action: Action
    access_allowed: bool

class AccessLogCreate(AccessLogBase):
    pass

class AccessLogUpdate(AccessLogBase):
    pass

class AccessLogUpdatePartical(BaseModel):
    user_id: int|None = None
    room_id: int|None = None
    action: Action|None = None
    access_allowed: bool|None = None

class AccessLogOut(AccessLogBase):
    id: int
    timestamp: datetime

class AccessLogWithUser(AccessLogOut):
    user: User

class AccessLogWithRoom(AccessLogOut):
    room: Room