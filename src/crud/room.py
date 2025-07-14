from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, Result

from models import Room
from schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomUpdatePartical
)

async def create_room(
        session: AsyncSession, 
        room_in: RoomCreate
) -> Room:
    room = Room(**room_in.model_dump())
    session.add(room)
    await session.commit()
    await session.refresh(room)

    return room

async def update_room(
        session: AsyncSession,
        room: Room,
        room_in: RoomUpdate|RoomUpdatePartical,
        partical: bool = False,
) -> Room:
    for name, value in room_in.model_dump(exclude_none=partical).items():
        setattr(room, name, value)
    await session.commit()
    await session.refresh(room)
    return room

async def delete_room(
        session: AsyncSession,
        room: Room,
) -> None:
    await session.delete(room)
    await session.commit()

async def get_room(
        session: AsyncSession, 
        room_id: int
) -> Room|None:
    return await session.get(Room, room_id)

async def get_rooms(
        session: AsyncSession, 
        offset: int = 0, 
        limit: int = 100
) -> Sequence[Room]:
    stmt = (
        select(Room)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(statement=stmt)
    return rooms.all()

async def get_room_with_floor(
        session: AsyncSession,
        room_id: int
) -> Room|None:
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(joinedload(Room.floor))
    )
    room = await session.scalar(statement=stmt)
    return room

async def get_room_with_access_logs(
        session: AsyncSession,
        room_id: int
) -> Room|None:
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.access_logs))
    )
    return await session.scalar(statement=stmt)

async def get_room_with_access_rules(
        session: AsyncSession,
        room_id: int
) -> Room|None:
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.access_rules))
    )
    return await session.scalar(statement=stmt)

async def get_room_with_access_current_presence(
        session: AsyncSession,
        room_id: int
) -> Room|None:
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.current_presence))
    )
    return await session.scalar(statement=stmt)


async def get_rooms_with_access_rules(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    stmt = (
        select(Room)
        .options(selectinload(Room.access_rules))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(statement=stmt)
    return rooms.all()

async def get_rooms_with_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    stmt = (
        select(Room)
        .options(selectinload(Room.access_logs))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(statement=stmt)
    return rooms.all()

async def get_rooms_with_current_presence(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    stmt = (
        select(Room)
        .options(selectinload(Room.current_presence))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(statement=stmt)
    return rooms.all()

async def get_rooms_with_floor(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    stmt = (
        select(Room)
        .options(joinedload(Room.floor))
        .offset(offset=offset)
        .limit(limit=limit)
    )
    rooms = await session.scalars(statement=stmt)
    return rooms.all()
    