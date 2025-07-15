from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from src.models import CurrentPresence
from src.schemas.current_presence import (
    CurrentPresenceCreate,
    CurrentPresenceUpdate,
    CurrentPresenceUpdatePartical,
)

async def create_current_presence(
        session: AsyncSession,
        current_presence_in: CurrentPresenceCreate,
) -> CurrentPresence:
    current_presence = CurrentPresence(**current_presence_in.model_dump())
    session.add(current_presence)
    await session.commit()
    await session.refresh(current_presence)
    return current_presence

async def update_current_presence(
        session: AsyncSession,
        current_presence: CurrentPresence,
        current_presence_in: CurrentPresenceUpdate|CurrentPresenceUpdatePartical,
        partical: bool = False
) -> CurrentPresence:
    for name, value in current_presence_in.model_dump(exclude_none=partical).items():
        setattr(current_presence, name, value)
    await session.commit()
    await session.refresh(current_presence)
    return current_presence

async def delete_current_presence(
        session: AsyncSession,
        current_presence: CurrentPresence,
) -> None:
    await session.delete(current_presence)
    await session.commit()

async def get_current_presence(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence| None:
    current_presence = await session.get(CurrentPresence, current_presence_id)
    return current_presence

async def get_current_presences(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    stmt = (
        select(CurrentPresence)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(statement=stmt)
    return current_presences.all()

async def get_current_presence_with_room(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence|None:
    stmt = (
        select(CurrentPresence)
        .where(CurrentPresence.id == current_presence_id)
        .options(joinedload(CurrentPresence.room))
    )
    current_presence = await session.scalar(statement=stmt)

    return current_presence

async def get_current_presence_with_user(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence|None:
    stmt = (
        select(CurrentPresence)
        .where(CurrentPresence.id == current_presence_id)
        .options(joinedload(CurrentPresence.user))
    )
    current_presence = await session.scalar(statement=stmt)

    return current_presence

async def get_current_presences_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    stmt = (
        select(CurrentPresence)
        .options(joinedload(CurrentPresence.room))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(statement=stmt)

    return current_presences.all()

async def get_current_presences_with_user(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    stmt = (
        select(CurrentPresence)
        .options(joinedload(CurrentPresence.user))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(statement=stmt)

    return current_presences.all()