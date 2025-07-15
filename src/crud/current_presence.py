"""
CRUD operations for CurrentPresence model with comprehensive error handling.
"""

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from src.models import CurrentPresence
from src.schemas.current_presence import (
    CurrentPresenceCreate,
    CurrentPresenceUpdate,
    CurrentPresenceUpdatePartical,
)
import src.crud.exceptions as exceptions

async def create_current_presence(
        session: AsyncSession,
        current_presence_in: CurrentPresenceCreate,
) -> CurrentPresence:
    """
    Create a new current presence record in database.
    
    Args:
        session: Async database session
        current_presence_in: CurrentPresenceCreate schema with data
        
    Returns:
        CurrentPresence: Newly created CurrentPresence object
        
    Raises:
        CurrentPresenceAlreadyExistsException: If presence for user exists
        CurrentPresenceConflictException: If user is in another room
        CreateException: If general creation error occurs
    """
    try:
        current_presence = CurrentPresence(**current_presence_in.model_dump())
        session.add(current_presence)
        await session.commit()
        await session.refresh(current_presence)
        return current_presence
    except IntegrityError as e:
        await session.rollback()
        if "user_id" in str(e).lower():
            raise exceptions.CurrentPresenceAlreadyExistsException(
                user_id=current_presence_in.user_id
            ) from e
        if "room_id" in str(e).lower():
            raise exceptions.CurrentPresenceConflictException(
                user_id=current_presence_in.user_id,
                room_id=current_presence_in.room_id
            ) from e
        raise exceptions.CreateException(model_name="CurrentPresence", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="CurrentPresence", original_exc=e) from e

async def update_current_presence(
        session: AsyncSession,
        current_presence: CurrentPresence,
        current_presence_in: CurrentPresenceUpdate | CurrentPresenceUpdatePartical,
        partial: bool = False
) -> CurrentPresence:
    """
    Update existing current presence record.
    
    Args:
        session: Async database session
        current_presence: CurrentPresence object to update
        current_presence_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        CurrentPresence: Updated CurrentPresence object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in current_presence_in.model_dump(exclude_none=partial).items():
            setattr(current_presence, name, value)
        await session.commit()
        await session.refresh(current_presence)
        return current_presence
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="CurrentPresence",
            entity_id=current_presence.id,
            original_exc=e
        ) from e

async def delete_current_presence(
        session: AsyncSession,
        current_presence: CurrentPresence,
) -> None:
    """
    Delete current presence record from database.
    
    Args:
        session: Async database session
        current_presence: CurrentPresence object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(current_presence)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="CurrentPresence",
            entity_id=current_presence.id,
            original_exc=e
        ) from e

async def get_current_presence(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence | None:
    """
    Get current presence record by ID.
    
    Args:
        session: Async database session
        current_presence_id: ID of record to retrieve
        
    Returns:
        CurrentPresence | None: CurrentPresence object if found, None otherwise
    """
    return await session.get(CurrentPresence, current_presence_id)

async def get_current_presences(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    """
    Get paginated list of current presence records.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of records to return
        
    Returns:
        Sequence[CurrentPresence]: List of CurrentPresence objects
    """
    stmt = (
        select(CurrentPresence)
        .offset(offset)
        .limit(limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(stmt)
    return current_presences.all()

async def get_current_presence_with_room(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence | None:
    """
    Get current presence record with room loaded.
    
    Args:
        session: Async database session
        current_presence_id: ID of record to retrieve
        
    Returns:
        CurrentPresence | None: CurrentPresence object with room if found, None otherwise
    """
    stmt = (
        select(CurrentPresence)
        .where(CurrentPresence.id == current_presence_id)
        .options(joinedload(CurrentPresence.room))
    )
    return await session.scalar(stmt)

async def get_current_presence_with_user(
        session: AsyncSession,
        current_presence_id: int
) -> CurrentPresence | None:
    """
    Get current presence record with user loaded.
    
    Args:
        session: Async database session
        current_presence_id: ID of record to retrieve
        
    Returns:
        CurrentPresence | None: CurrentPresence object with user if found, None otherwise
    """
    stmt = (
        select(CurrentPresence)
        .where(CurrentPresence.id == current_presence_id)
        .options(joinedload(CurrentPresence.user))
    )
    return await session.scalar(stmt)

async def get_current_presences_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    """
    Get paginated list of current presence records with rooms loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of records to return
        
    Returns:
        Sequence[CurrentPresence]: List of CurrentPresence objects with rooms
    """
    stmt = (
        select(CurrentPresence)
        .options(joinedload(CurrentPresence.room))
        .offset(offset)
        .limit(limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(stmt)
    return current_presences.all()

async def get_current_presences_with_user(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[CurrentPresence]:
    """
    Get paginated list of current presence records with users loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of records to return
        
    Returns:
        Sequence[CurrentPresence]: List of CurrentPresence objects with users
    """
    stmt = (
        select(CurrentPresence)
        .options(joinedload(CurrentPresence.user))
        .offset(offset)
        .limit(limit)
        .order_by(CurrentPresence.timestamp.desc())
    )
    current_presences = await session.scalars(stmt)
    return current_presences.all()