from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models import AccessLog
from schemas.access_log import (
    AccessLogCreate,
    AccessLogUpdate,
    AccessLogUpdatePartical,
)

async def create_access_log(
        session: AsyncSession,
        access_log_in: AccessLogCreate,
) -> AccessLog:
    access_log = AccessLog(**access_log_in.model_dump())
    session.add(access_log)
    await session.commit()
    await session.refresh(access_log)

    return access_log

async def update_access_log(
        session: AsyncSession,
        access_log: AccessLog,
        access_log_in: AccessLogUpdate|AccessLogUpdatePartical,
        partical: bool = False,
) -> AccessLog:
    for name, value in access_log_in.model_dump(exclude_none=partical).items():
        setattr(access_log, name, value)
    await session.commit()
    await session.refresh(access_log)

    return access_log

async def delete_access_log(
        session: AsyncSession,
        access_log: AccessLog
) -> None:
    await session.delete(access_log)
    await session.commit()

async def get_access_log(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog|None:
    return await session.get(AccessLog, access_log_id)

async def get_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) ->  Sequence[AccessLog]:
    stmt = (
        select(AccessLog)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(stmt)
    return access_logs.all()

async def get_access_log_with_room(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog|None:
    stmt = (
        select(AccessLog)
        .where(AccessLog.id == access_log_id)
        .options(joinedload(AccessLog.room))
    )
    return await session.scalar(statement=stmt)

async def get_access_log_with_user(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog|None:
    stmt = (
        select(AccessLog)
        .where(AccessLog.id == access_log_id)
        .options(joinedload(AccessLog.user))
    )
    return await session.scalar(statement=stmt)

async def get_access_logs_with_user(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessLog]:
    stmt = (
        select(AccessLog)
        .options(joinedload(AccessLog.user))
        .offset(offset)
        .limit(limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(statement=stmt)
    return access_logs.all()

async def get_access_logs_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessLog]:
    stmt = (
        select(AccessLog)
        .options(joinedload(AccessLog.room))
        .offset(offset)
        .limit(limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(statement=stmt)
    return access_logs.all()