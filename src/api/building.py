from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from database.core import DBSession
from crud import building as crud
from models import Building
import schemas.building as schemas  
from .dependencies import get_building_by_id

router = APIRouter(prefix="/buildings", tags=["Buildings"])

@router.post("/", response_model=schemas.BuildingOut)
async def create_building(
    session: DBSession,
    building_in: schemas.BuildingCreate,
):
    return await crud.create_building(session, building_in)

@router.put("/{building_id}", response_model=schemas.BuildingOut)
async def update_building(
    session: DBSession,
    building_in: schemas.BuildingUpdate,
    building: Building = Depends(get_building_by_id) 
):
    return await crud.update_building(
        session, 
        building_in=building_in, 
        building=building
    )

@router.patch("/{building_id}", response_model=schemas.BuildingOut)
async def update_building_partical(
    session: DBSession,
    building_in: schemas.BuildingUpdatePartical,
    building: Building = Depends(get_building_by_id) 
):
    return await crud.update_building(
        session, 
        building_in=building_in, 
        building=building,
        partical=True
    )

@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    session: DBSession,
    building: Building = Depends(get_building_by_id)
):
    await crud.delete_building(session, building)

@router.get("/", response_model=list[schemas.BuildingOut])
async def get_buildings(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    buildings = await crud.get_buildings(session, offset, limit)
    return list(buildings)

@router.get("/with-floors", response_model=list[schemas.BuildingWithFloors])
async def get_building_with_floors(
    sessison: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    buildings = await crud.get_buildings_with_floors(sessison, offset, limit)
    return list(buildings)

@router.get("/{building_id}", response_model=schemas.BuildingOut)
async def get_building(
    building: Building = Depends(get_building_by_id)
):
    return building
