from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from src.models import Floor
from src.schemas.floor import (
    FloorCreate,
    FloorUpdate,
    FloorUpdatePartical,
)

async def create_floor(
        session: AsyncSession,
        floor_in: FloorCreate
) -> Floor:
    floor = Floor(**floor_in.model_dump())
    session.add(floor)
    await session.commit()
    await session.refresh(floor)

    return floor

async def update_floor(
        session: AsyncSession,
        floor: Floor,
        floor_in: FloorUpdate|FloorUpdatePartical,
        partical: bool = False,
) -> Floor:
    for name, value in floor_in.model_dump(exclude_none=partical).items():
        setattr(floor, name, value)
    await session.commit()
    await session.refresh(floor)
    return floor

async def delete_floor(
        session: AsyncSession,
        floor: Floor
) -> None:
    await session.delete(floor)
    await session.commit()

async def get_floor(
        session: AsyncSession,
        floor_id: int
) -> Floor|None:
    return await session.get(Floor, floor_id)

async def get_floors(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Floor]:
    stmt = (
        select(Floor)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Floor.id)
    )

    floors = await session.scalars(statement=stmt)
    return floors.all()


async def get_floor_with_rooms(
        session: AsyncSession,
        floor_id: int
)-> Floor|None:
    stmt = (
        select(Floor)
        .where(Floor.id == floor_id)
        .options(selectinload(Floor.rooms))
    )
    return await session.scalar(statement=stmt)

async def get_floor_with_building(
        session: AsyncSession,
        floor_id: int
)-> Floor|None:
    stmt = (
        select(Floor)
        .where(Floor.id == floor_id)
        .options(joinedload(Floor.building))
    )
    return await session.scalar(statement=stmt)

async def get_floors_with_rooms(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
)-> Sequence[Floor]:
    stmt = (
        select(Floor)
        .options(selectinload(Floor.rooms))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Floor.id)
    )
    floors = await session.scalars(statement=stmt)
    return floors.all()

async def get_floors_with_building(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
)-> Sequence[Floor]:
    stmt = (
        select(Floor)
        .options(joinedload(Floor.building))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Floor.id)
    )
    floors = await session.scalars(statement=stmt)

    return floors.all()