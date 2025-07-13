from typing import Annotated
from annotated_types import Ge

from pydantic import BaseModel

from .general_schemas import (
    Building, 
    Room,
)


class FloorBase(BaseModel):
    floor_number: Annotated[int, Ge(0)]
    building_id: int

class FloorCreate(FloorBase):
    pass

class FloorUpdate(FloorBase):
    pass

class FloorUpdatePartical(BaseModel):
    floor_number: Annotated[int|None, Ge(0)] = None
    building_id: int|None = None

class FloorOut(FloorBase):
    id: int

class FloorWithBuilding(FloorOut):
    building: Building

class FloorWithRooms(FloorOut):
    rooms: list[Room]