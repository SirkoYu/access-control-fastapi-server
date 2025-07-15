from typing import Sequence

from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import src.crud.exceptions as exceptions
from src.models import AccessLog
from src.schemas.access_log import (
    AccessLogCreate,
    AccessLogUpdate,
    AccessLogUpdatePartical,
)

async def create_access_log(
        session: AsyncSession,
        access_log_in: AccessLogCreate,
) -> AccessLog:
    """
    Create a new access log entry in the database.
    
    Args:
        session: Async database session
        access_log_in: AccessLogCreate schema with log data
        
    Returns:
        AccessLog: Newly created AccessLog object
        
    Raises:
        CreateException: If creation error occurs
    """
    try:
        access_log = AccessLog(**access_log_in.model_dump())
        session.add(access_log)
        await session.commit()
        await session.refresh(access_log)
        return access_log
    except IntegrityError as e:
        await session.rollback()
        raise exceptions.AccessLogInvalidReferancesException(e) from e
    except OperationalError as e:
        raise exceptions.OperationalException(model_name="AccessLog", original_exc=e)
    except DatabaseError as e:
        await session.rollback()
        raise exceptions.CreateException(
            model_name="AccessLog",
            original_exc=e
        ) from e

async def update_access_log(
        session: AsyncSession,
        access_log: AccessLog,
        access_log_in: AccessLogUpdate | AccessLogUpdatePartical,
        partial: bool = False,
) -> AccessLog:
    """
    Update existing access log entry.
    
    Args:
        session: Async database session
        access_log: AccessLog object to update
        access_log_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        AccessLog: Updated AccessLog object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in access_log_in.model_dump(exclude_none=partial).items():
            setattr(access_log, name, value)
        await session.commit()
        await session.refresh(access_log)
        return access_log
    except OperationalError as e:
        raise exceptions.OperationalException(model_name="AccessLog", original_exc=e)
    except DatabaseError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="AccessLog",
            entity_id=access_log.id,
            original_exc=e
        ) from e

async def delete_access_log(
        session: AsyncSession,
        access_log: AccessLog
) -> None:
    """
    Delete access log entry from database.
    
    Args:
        session: Async database session
        access_log: AccessLog object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(access_log)
        await session.commit()
    except OperationalError as e:
        raise exceptions.OperationalException(model_name="AccessLog", original_exc=e)
    except DatabaseError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="AccessLog",
            entity_id=access_log.id,
            original_exc=e
        ) from e

async def get_access_log(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog | None:
    """
    Get access log by ID.
    
    Args:
        session: Async database session
        access_log_id: ID of log entry to retrieve
        
    Returns:
        AccessLog | None: AccessLog object if found, None otherwise
    """
    return await session.get(AccessLog, access_log_id)

async def get_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessLog]:
    """
    Get paginated list of access logs ordered by timestamp (newest first).
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of logs to return
        
    Returns:
        Sequence[AccessLog]: List of AccessLog objects
    """
    stmt = (
        select(AccessLog)
        .offset(offset)
        .limit(limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(stmt)
    return access_logs.all()

async def get_access_log_with_room(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog | None:
    """
    Get access log with room information loaded.
    
    Args:
        session: Async database session
        access_log_id: ID of log entry to retrieve
        
    Returns:
        AccessLog | None: AccessLog object with room if found, None otherwise
    """
    stmt = (
        select(AccessLog)
        .where(AccessLog.id == access_log_id)
        .options(joinedload(AccessLog.room))
    )
    return await session.scalar(stmt)

async def get_access_log_with_user(
        session: AsyncSession,
        access_log_id: int
) -> AccessLog | None:
    """
    Get access log with user information loaded.
    
    Args:
        session: Async database session
        access_log_id: ID of log entry to retrieve
        
    Returns:
        AccessLog | None: AccessLog object with user if found, None otherwise
    """
    stmt = (
        select(AccessLog)
        .where(AccessLog.id == access_log_id)
        .options(joinedload(AccessLog.user))
    )
    return await session.scalar(stmt)

async def get_access_logs_with_user(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessLog]:
    """
    Get paginated list of access logs with user information loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of logs to return
        
    Returns:
        Sequence[AccessLog]: List of AccessLog objects with users
    """
    stmt = (
        select(AccessLog)
        .options(joinedload(AccessLog.user))
        .offset(offset)
        .limit(limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(stmt)
    return access_logs.all()

async def get_access_logs_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessLog]:
    """
    Get paginated list of access logs with room information loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of logs to return
        
    Returns:
        Sequence[AccessLog]: List of AccessLog objects with rooms
    """
    stmt = (
        select(AccessLog)
        .options(joinedload(AccessLog.room))
        .offset(offset)
        .limit(limit)
        .order_by(AccessLog.timestamp.desc())
    )
    access_logs = await session.scalars(stmt)
    return access_logs.all()