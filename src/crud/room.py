"""
CRUD operations for Room model with comprehensive error handling.
"""

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select

from src.models import Room
from src.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomUpdatePartical
)
import src.crud.exceptions as exceptions

async def create_room(
        session: AsyncSession, 
        room_in: RoomCreate
) -> Room:
    """
    Create a new room in the database.
    
    Args:
        session: Async database session
        room_in: RoomCreate schema with room data
        
    Returns:
        Room: Newly created Room object
        
    Raises:
        RoomAlreadyExistsException: If room with same attributes exists
        CreateException: If general creation error occurs
    """
    try:
        room = Room(**room_in.model_dump())
        session.add(room)
        await session.commit()
        await session.refresh(room)
        return room
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
            raise exceptions.RoomAlreadyExistsException() from e
        raise exceptions.CreateException(model_name="Room", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="Room", original_exc=e) from e


async def update_room(
        session: AsyncSession,
        room: Room,
        room_in: RoomUpdate | RoomUpdatePartical,
        partial: bool = False,
) -> Room:
    """
    Update existing room data.
    
    Args:
        session: Async database session
        room: Room object to update
        room_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        Room: Updated Room object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in room_in.model_dump(exclude_none=partial).items():
            setattr(room, name, value)
        await session.commit()
        await session.refresh(room)
        return room
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="Room",
            entity_id=room.id,
            original_exc=e
        ) from e


async def delete_room(
        session: AsyncSession,
        room: Room,
) -> None:
    """
    Delete room from database.
    
    Args:
        session: Async database session
        room: Room object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(room)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="Room",
            entity_id=room.id,
            original_exc=e
        ) from e


async def get_room(
        session: AsyncSession, 
        room_id: int
) -> Room | None:
    """
    Get room by ID.
    
    Args:
        session: Async database session
        room_id: ID of room to retrieve
        
    Returns:
        Room | None: Room object if found, None otherwise
    """
    return await session.get(Room, room_id)

async def get_rooms(
        session: AsyncSession, 
        offset: int = 0, 
        limit: int = 100
) -> Sequence[Room]:
    """
    Get paginated list of rooms.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rooms to return
        
    Returns:
        Sequence[Room]: List of Room objects
    """
    stmt = (
        select(Room)
        .offset(offset)
        .limit(limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(stmt)
    return rooms.all()


async def get_room_with_floor(
        session: AsyncSession,
        room_id: int
) -> Room | None:
    """
    Get room with floor information loaded.
    
    Args:
        session: Async database session
        room_id: ID of room to retrieve
        
    Returns:
        Room | None: Room object with floor if found, None otherwise
    """
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(joinedload(Room.floor)))
    return await session.scalar(stmt)


async def get_room_with_access_logs(
        session: AsyncSession,
        room_id: int
) -> Room | None:
    """
    Get room with access logs loaded.
    
    Args:
        session: Async database session
        room_id: ID of room to retrieve
        
    Returns:
        Room | None: Room object with access logs if found, None otherwise
    """
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.access_logs))
    )
    return await session.scalar(stmt)


async def get_room_with_access_rules(
        session: AsyncSession,
        room_id: int
) -> Room | None:
    """
    Get room with access rules loaded.
    
    Args:
        session: Async database session
        room_id: ID of room to retrieve
        
    Returns:
        Room | None: Room object with access rules if found, None otherwise
    """
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.access_rules))
    )
    return await session.scalar(stmt)


async def get_room_with_current_presence(
        session: AsyncSession,
        room_id: int
) -> Room | None:
    """
    Get room with current presence information loaded.
    
    Args:
        session: Async database session
        room_id: ID of room to retrieve
        
    Returns:
        Room | None: Room object with current presence if found, None otherwise
    """
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.current_presence))
    )
    return await session.scalar(stmt)


async def get_rooms_with_access_rules(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    """
    Get paginated list of rooms with access rules loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rooms to return
        
    Returns:
        Sequence[Room]: List of Room objects with access rules
    """
    stmt = (
        select(Room)
        .options(selectinload(Room.access_rules))
        .offset(offset)
        .limit(limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(stmt)
    return rooms.all()


async def get_rooms_with_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    """
    Get paginated list of rooms with access logs loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rooms to return
        
    Returns:
        Sequence[Room]: List of Room objects with access logs
    """
    stmt = (
        select(Room)
        .options(selectinload(Room.access_logs))
        .offset(offset)
        .limit(limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(stmt)
    return rooms.all()


async def get_rooms_with_current_presence(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    """
    Get paginated list of rooms with current presence loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rooms to return
        
    Returns:
        Sequence[Room]: List of Room objects with current presence
    """
    stmt = (
        select(Room)
        .options(selectinload(Room.current_presence))
        .offset(offset)
        .limit(limit)
        .order_by(Room.id)
    )
    rooms = await session.scalars(stmt)
    return rooms.all()


async def get_rooms_with_floor(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Room]:
    """
    Get paginated list of rooms with floor information loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rooms to return
        
    Returns:
        Sequence[Room]: List of Room objects with floor information
    """
    stmt = (
        select(Room)
        .options(joinedload(Room.floor))
        .offset(offset)
        .limit(limit)
    )
    rooms = await session.scalars(stmt)
    return rooms.all()