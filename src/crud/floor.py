from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from src.models import Floor
from src.schemas.floor import (
    FloorCreate,
    FloorUpdate,
    FloorUpdatePartical,
)
import src.crud.exceptions as exceptions


async def create_floor(
        session: AsyncSession,
        floor_in: FloorCreate
) -> Floor:
    """
    Create a new floor in the database.
    
    Args:
        session: Async database session
        floor_in: FloorCreate schema with floor data
        
    Returns:
        Floor: Newly created Floor object
        
    Raises:
        FloorAlreadyExistsException: If floor with same number in building exists
        CreateException: If general creation error occurs
    """
    try:
        floor = Floor(**floor_in.model_dump())
        session.add(floor)
        await session.commit()
        await session.refresh(floor)
        return floor
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower() and "number" in str(e).lower():
            raise exceptions.FloorAlreadyExistsException(
                floor_number=floor_in.floor_number,
                building_id=floor_in.building_id
            ) from e
        raise exceptions.CreateException(model_name="Floor", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="Floor", original_exc=e) from e

async def update_floor(
        session: AsyncSession,
        floor: Floor,
        floor_in: FloorUpdate | FloorUpdatePartical,
        partial: bool = False,
) -> Floor:
    """
    Update existing floor data.
    
    Args:
        session: Async database session
        floor: Floor object to update
        floor_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        Floor: Updated Floor object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in floor_in.model_dump(exclude_none=partial).items():
            setattr(floor, name, value)
        await session.commit()
        await session.refresh(floor)
        return floor
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="Floor",
            entity_id=floor.id,
            original_exc=e
        ) from e

async def delete_floor(
        session: AsyncSession,
        floor: Floor
) -> None:
    """
    Delete floor from database.
    
    Args:
        session: Async database session
        floor: Floor object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(floor)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="Floor",
            entity_id=floor.id,
            original_exc=e
        ) from e

async def get_floor(
        session: AsyncSession,
        floor_id: int
) -> Floor | None:
    """
    Get floor by ID.
    
    Args:
        session: Async database session
        floor_id: ID of floor to retrieve
        
    Returns:
        Floor | None: Floor object if found, None otherwise
    """
    return await session.get(Floor, floor_id)

async def get_floors(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Floor]:
    """
    Get paginated list of floors.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of floors to return
        
    Returns:
        Sequence[Floor]: List of Floor objects
    """
    stmt = (
        select(Floor)
        .offset(offset)
        .limit(limit)
        .order_by(Floor.id)
    )
    floors = await session.scalars(stmt)
    return floors.all()

async def get_floor_with_rooms(
        session: AsyncSession,
        floor_id: int
) -> Floor | None:
    """
    Get floor with rooms loaded.
    
    Args:
        session: Async database session
        floor_id: ID of floor to retrieve
        
    Returns:
        Floor | None: Floor object with rooms if found, None otherwise
    """
    stmt = (
        select(Floor)
        .where(Floor.id == floor_id)
        .options(selectinload(Floor.rooms))
    )
    return await session.scalar(stmt)

async def get_floor_with_building(
        session: AsyncSession,
        floor_id: int
) -> Floor | None:
    """
    Get floor with building loaded.
    
    Args:
        session: Async database session
        floor_id: ID of floor to retrieve
        
    Returns:
        Floor | None: Floor object with building if found, None otherwise
    """
    stmt = (
        select(Floor)
        .where(Floor.id == floor_id)
        .options(joinedload(Floor.building))
    )
    return await session.scalar(stmt)

async def get_floors_with_rooms(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Floor]:
    """
    Get paginated list of floors with rooms loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of floors to return
        
    Returns:
        Sequence[Floor]: List of Floor objects with rooms
    """
    stmt = (
        select(Floor)
        .options(selectinload(Floor.rooms))
        .offset(offset)
        .limit(limit)
        .order_by(Floor.id)
    )
    floors = await session.scalars(stmt)
    return floors.all()

async def get_floors_with_building(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Floor]:
    """
    Get paginated list of floors with building loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of floors to return
        
    Returns:
        Sequence[Floor]: List of Floor objects with building
    """
    stmt = (
        select(Floor)
        .options(joinedload(Floor.building))
        .offset(offset)
        .limit(limit)
        .order_by(Floor.id)
    )
    floors = await session.scalars(stmt)
    return floors.all()