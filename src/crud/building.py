"""
CRUD operations for Building model with comprehensive error handling.
"""

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

import src.crud.exceptions as exceptions
from src.models import Building
from src.schemas.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingUpdatePartical,
)

async def create_building(
        session: AsyncSession,
        building_in: BuildingCreate
) -> Building:
    """
    Create a new building in the database.
    
    Args:
        session: Async database session
        building_in: BuildingCreate schema with building data
        
    Returns:
        Building: Newly created Building object
        
    Raises:
        BuildingAlreadyExistsException: If building with same attributes exists
        CreateException: If general creation error occurs
    """
    try:
        building = Building(**building_in.model_dump())
        session.add(building)
        await session.commit()
        await session.refresh(building)
        return building
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
            raise exceptions.BuildingAlreadyExistsException(
                detail="Building with these attributes already exists"
            ) from e
        raise exceptions.CreateException(model_name="Building", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="Building", original_exc=e) from e

async def update_building(
        session: AsyncSession,
        building: Building,
        building_in: BuildingUpdate | BuildingUpdatePartical,
        partial: bool = False
) -> Building:
    """
    Update existing building data.
    
    Args:
        session: Async database session
        building: Building object to update
        building_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        Building: Updated Building object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in building_in.model_dump(exclude_none=partial).items():
            setattr(building, name, value)
        await session.commit()
        await session.refresh(building)
        return building
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="Building",
            entity_id=building.id,
            original_exc=e
        ) from e

async def delete_building(
        session: AsyncSession,
        building: Building,
) -> None:
    """
    Delete building from database.
    
    Args:
        session: Async database session
        building: Building object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(building)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="Building",
            entity_id=building.id,
            original_exc=e
        ) from e

async def get_building(
        session: AsyncSession,
        building_id: int,
) -> Building | None:
    """
    Get building by ID.
    
    Args:
        session: Async database session
        building_id: ID of building to retrieve
        
    Returns:
        Building | None: Building object if found, None otherwise
    """
    return await session.get(Building, building_id)

async def get_buildings(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Building]:
    """
    Get paginated list of buildings.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of buildings to return
        
    Returns:
        Sequence[Building]: List of Building objects
    """
    stmt = (
        select(Building)
        .offset(offset)
        .limit(limit)
        .order_by(Building.id)
    )
    buildings = await session.scalars(stmt)
    return buildings.all()

async def get_buildings_with_floors(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Building]:
    """
    Get paginated list of buildings with floors loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of buildings to return
        
    Returns:
        Sequence[Building]: List of Building objects with floors
    """
    stmt = (
        select(Building)
        .options(selectinload(Building.floors))
        .offset(offset)
        .limit(limit)
        .order_by(Building.id)
    )
    buildings = await session.scalars(stmt)
    return buildings.all()

async def get_building_with_floors(
        session: AsyncSession,
        building_id: int
) -> Building | None:
    """
    Get building with floors loaded.
    
    Args:
        session: Async database session
        building_id: ID of building to retrieve
        
    Returns:
        Building | None: Building object with floors if found, None otherwise
    """
    stmt = (
        select(Building)
        .where(Building.id == building_id)
        .options(selectinload(Building.floors))
    )
    return await session.scalar(stmt)