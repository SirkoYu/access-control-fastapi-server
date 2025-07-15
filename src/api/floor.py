from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from src.crud import floor as crud
from src.models import Floor
import src.schemas.floor as schemas 
from .dependencies import DBSession, get_floor_by_id

router = APIRouter(prefix="/floors", tags=["Floors"])

@router.post("/", response_model=schemas.FloorOut, status_code=status.HTTP_201_CREATED)
async def create_floor(
    session: DBSession,
    floor_in: schemas.FloorCreate,
):
    return await crud.create_floor(session, floor_in)

@router.put("/{floor_id}", response_model=schemas.FloorOut)
async def update_floor(
    session: DBSession,
    floor_in: schemas.FloorUpdate,
    floor: Floor = Depends(get_floor_by_id)
):
    return await crud.update_floor(session=session, floor_in= floor_in, floor=floor)

@router.patch("/{floor_id}", response_model=schemas.FloorOut)
async def update_floor_partical(
    session: DBSession,
    floor_in: schemas.FloorUpdatePartical,
    floor: Floor = Depends(get_floor_by_id)
):
    return await crud.update_floor(session=session, floor_in= floor_in, floor=floor, partical=True)

@router.delete("/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_floor(
    session: DBSession,
    floor: Floor = Depends(get_floor_by_id),
): 
    await crud.delete_floor(session, floor)

@router.get("/", response_model=list[schemas.FloorOut])
async def get_floors(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    floors = await crud.get_floors(session, offset, limit)
    return list(floors)

@router.get("/with-building", response_model=list[schemas.FloorWithBuilding])
async def get_floors_with_buildings(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    floors = await crud.get_floors_with_building(session, offset, limit)
    return list(floors)

@router.get("/with-rooms", response_model=list[schemas.FloorWithRooms])
async def get_floors_with_rooms(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    floors = await crud.get_floors_with_rooms(session, offset, limit)
    return list(floors)

@router.get("/{floor_id}", response_model=schemas.FloorOut)
async def get_floor(
    floor: Floor = Depends(get_floor_by_id)
): 
    return floor