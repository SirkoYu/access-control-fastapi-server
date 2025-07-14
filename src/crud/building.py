from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models import Building
from schemas.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingUpdatePartical,
)

async def create_building(
        session: AsyncSession,
        building_in: BuildingCreate
) -> Building:
    building = Building(**building_in.model_dump())
    session.add(building)
    await session.commit()
    await session.refresh(building)

    return building

async def update_building(
        session: AsyncSession,
        building: Building,
        building_in: BuildingUpdate|BuildingUpdatePartical,
        partical:bool = False
) -> Building:
    for name, value in building_in.model_dump(exclude_none=partical).items():
        setattr(building, name, value)
    await session.commit()
    await session.refresh(building)

    return  building

async def delete_building(
        session: AsyncSession,
        building: Building,
) -> None:
    await session.delete(building)
    await session.commit()

async def get_building(
        session: AsyncSession,
        building_id: int,
) -> Building|None:
    return await session.get(Building, building_id)

async def get_buildings(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Building]:
    stmt = (
        select(Building)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Building.id)
    )

    buildings = await session.scalars(statement=stmt)
    return buildings.all()

async def get_buildings_with_floors(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Building]:
    stmt = (
        select(Building)
        .options(selectinload(Building.floors))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Building.id)
    )

    buildings = await session.scalars(statement=stmt)
    return buildings.all()

async def get_building_with_floor(
        session: AsyncSession,
        building_id: int
) -> Building|None:
    stmt = (
        select(Building)
        .where(Building.id == building_id)
        .options(selectinload(Building.floors))
    )
    return await session.scalar(statement=stmt)