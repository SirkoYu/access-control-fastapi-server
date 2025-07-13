from datetime import datetime

from pydantic import BaseModel

from .general_schemas import (
    User, 
    Room,
)

class CurrentPresenceBase(BaseModel):
    room_id: int
    user_id: int

class CurrentPresenceCreate(CurrentPresenceBase):
    pass

class CurrentPresenceUpdate(CurrentPresenceBase):
    pass

class CurrentPresenceUpdatePartical(BaseModel):
    room_id: int|None = None
    user_id: int|None = None

class CurrentPresenceOut(CurrentPresenceBase):
    id: int
    timestamp: datetime

class CurrentPresenceWithUser(CurrentPresenceOut):
    user: User

class CurrentPresenceWithRoom(CurrentPresenceOut):
    room: Room