from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models import Role
from src.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleUpdatePartical,
)
import src.crud.exceptions as exceptions


async def create_role(
        session: AsyncSession, 
        role_in: RoleCreate
) -> Role:
    """
    Create a new role in the database.
    
    Args:
        session: Async database session
        role_in: RoleCreate schema with role data
        
    Returns:
        Role: Newly created Role object
        
    Raises:
        RoleAlreadyExistsException: If role with same name exists
        CreateException: If general creation error occurs
    """
    try:
        role = Role(**role_in.model_dump())
        session.add(role)
        await session.commit()
        await session.refresh(role)
        return role
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower() and "name" in str(e).lower():
            raise exceptions.RoleAlreadyExistsException(name=role_in.name) from e
        raise exceptions.CreateException(model_name="Role", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="Role", original_exc=e) from e

async def update_role(
        session: AsyncSession,
        role: Role,
        role_in: RoleUpdate | RoleUpdatePartical,
        partial: bool = False,
) -> Role:
    """
    Update existing role data.
    
    Args:
        session: Async database session
        role: Role object to update
        role_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        Role: Updated Role object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in role_in.model_dump(exclude_none=partial).items():
            setattr(role, name, value)
        await session.commit()
        await session.refresh(role)
        return role
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="Role",
            entity_id=role.id,
            original_exc=e
        ) from e

async def delete_role(
        session: AsyncSession, 
        role: Role
) -> None:
    """
    Delete role from database.
    
    Args:
        session: Async database session
        role: Role object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(role)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="Role",
            entity_id=role.id,
            original_exc=e
        ) from e

async def get_role(
        session: AsyncSession, 
        role_id: int
) -> Role | None:
    """
    Get role by ID.
    
    Args:
        session: Async database session
        role_id: ID of role to retrieve
        
    Returns:
        Role | None: Role object if found, None otherwise
    """
    return await session.get(Role, role_id)

async def get_roles(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Role]:
    """
    Get paginated list of roles.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of roles to return
        
    Returns:
        Sequence[Role]: List of Role objects
    """
    stmt = (
        select(Role)
        .offset(offset)
        .limit(limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(stmt)
    return roles.all()

async def get_role_with_access_rules(
        session: AsyncSession,
        role_id: int
) -> Role | None:
    """
    Get role with access rules loaded.
    
    Args:
        session: Async database session
        role_id: ID of role to retrieve
        
    Returns:
        Role | None: Role object with access rules if found, None otherwise
    """
    stmt = (
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.access_rules))
    )
    return await session.scalar(stmt)

async def get_role_with_users(
        session: AsyncSession,
        role_id: int
) -> Role | None:
    """
    Get role with users loaded.
    
    Args:
        session: Async database session
        role_id: ID of role to retrieve
        
    Returns:
        Role | None: Role object with users if found, None otherwise
    """
    stmt = (
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.users))
    )
    return await session.scalar(stmt)

async def get_roles_with_access_rules(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Role]:
    """
    Get paginated list of roles with access rules loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of roles to return
        
    Returns:
        Sequence[Role]: List of Role objects with access rules
    """
    stmt = (
        select(Role)
        .options(selectinload(Role.access_rules))
        .offset(offset)
        .limit(limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(stmt)
    return roles.all()

async def get_roles_with_users(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Role]:
    """
    Get paginated list of roles with users loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of roles to return
        
    Returns:
        Sequence[Role]: List of Role objects with users
    """
    stmt = (
        select(Role)
        .options(selectinload(Role.users))
        .offset(offset)
        .limit(limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(stmt)
    return roles.all()