from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel

from .general_schemas import Floor

class BuildingBase(BaseModel):
    name: Annotated[str, MaxLen(48), MinLen(3)]
    description: str
    address: Annotated[str, MaxLen(64), MinLen(3)]

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BuildingBase):
    pass

class BuildingUpdatePartical(BaseModel):
    name: Annotated[str|None, MaxLen(48), MinLen(3)] = None
    description: str|None = None
    address: Annotated[str|None, MaxLen(64), MinLen(3)] = None

class BuildingOut(BuildingBase):
    id: int

class BuildingWithFloors(BuildingOut):
    floors: list[Floor]