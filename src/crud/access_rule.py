"""
CRUD operations for AccessRule model with comprehensive error handling.
"""

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import src.crud.exceptions as exceptions
from src.models import AccessRule
from src.schemas.access_rule import (
    AccessRuleCreate,
    AccessRuleUpdate,
    AccessRuleUpdatePartical,
)


async def create_access_rule(
        session: AsyncSession,
        access_rule_in: AccessRuleCreate,
) -> AccessRule:
    """
    Create a new access rule in the database.
    
    Args:
        session: Async database session
        access_rule_in: AccessRuleCreate schema with rule data
        
    Returns:
        AccessRule: Newly created AccessRule object
        
    Raises:
        AccessRuleAlreadyExistsException: If rule for room+role exists
        AccessRuleTimeConflictException: If time range conflicts
        CreateException: If general creation error occurs
    """
    try:
        access_rule = AccessRule(**access_rule_in.model_dump())
        session.add(access_rule)
        await session.commit()
        await session.refresh(access_rule)
        return access_rule
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower() and "room_id" in str(e).lower():
            raise exceptions.AccessRuleAlreadyExistsException(
                room_id=access_rule_in.room_id,
                role_id=access_rule_in.role_id
            ) from e
        if "time conflict" in str(e).lower():
            raise exceptions.AccessRuleTimeConflictException(
                room_id=access_rule_in.room_id,
                role_id=access_rule_in.role_id
            ) from e
        raise exceptions.CreateException(model_name="AccessRule", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="AccessRule", original_exc=e) from e

async def update_access_rule(
        session: AsyncSession,
        access_rule: AccessRule,
        access_rule_in: AccessRuleUpdate | AccessRuleUpdatePartical,
        partial: bool = False,
) -> AccessRule:
    """
    Update existing access rule.
    
    Args:
        session: Async database session
        access_rule: AccessRule object to update
        access_rule_in: Update data (full or partial)
        partial: Whether to perform partial update
        
    Returns:
        AccessRule: Updated AccessRule object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in access_rule_in.model_dump(exclude_none=partial).items():
            setattr(access_rule, name, value)
        await session.commit()
        await session.refresh(access_rule)
        return access_rule
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="AccessRule",
            entity_id=access_rule.id,
            original_exc=e
        ) from e

async def delete_access_rule(
        session: AsyncSession,
        access_rule: AccessRule,
) -> None:
    """
    Delete access rule from database.
    
    Args:
        session: Async database session
        access_rule: AccessRule object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(access_rule)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="AccessRule",
            entity_id=access_rule.id,
            original_exc=e
        ) from e

async def get_access_rule(
        session: AsyncSession,
        access_rule_id: int
) -> AccessRule | None:
    """
    Get access rule by ID.
    
    Args:
        session: Async database session
        access_rule_id: ID of rule to retrieve
        
    Returns:
        AccessRule | None: AccessRule object if found, None otherwise
    """
    return await session.get(AccessRule, access_rule_id)

async def get_access_rules(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    """
    Get paginated list of access rules.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rules to return
        
    Returns:
        Sequence[AccessRule]: List of AccessRule objects
    """
    stmt = (
        select(AccessRule)
        .offset(offset)
        .limit(limit)
        .order_by(AccessRule.id)
    )
    access_rules = await session.scalars(stmt)
    return access_rules.all()

async def get_access_rules_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    """
    Get paginated list of access rules with room loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rules to return
        
    Returns:
        Sequence[AccessRule]: List of AccessRule objects with room
    """
    stmt = (
        select(AccessRule)
        .options(joinedload(AccessRule.room))
        .offset(offset)
        .limit(limit)
        .order_by(AccessRule.id)
    )
    access_rules = await session.scalars(stmt)
    return access_rules.all()

async def get_access_rules_with_role(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    """
    Get paginated list of access rules with role loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of rules to return
        
    Returns:
        Sequence[AccessRule]: List of AccessRule objects with role
    """
    stmt = (
        select(AccessRule)
        .options(joinedload(AccessRule.role))
        .offset(offset)
        .limit(limit)
        .order_by(AccessRule.id)
    )
    access_rules = await session.scalars(stmt)
    return access_rules.all()

async def get_access_rule_with_room(
        session: AsyncSession,
        access_rule_id: int,
) -> AccessRule | None:
    """
    Get access rule with room loaded.
    
    Args:
        session: Async database session
        access_rule_id: ID of rule to retrieve
        
    Returns:
        AccessRule | None: AccessRule object with room if found, None otherwise
    """
    stmt = (
        select(AccessRule)
        .where(AccessRule.id == access_rule_id)
        .options(joinedload(AccessRule.room))
    )
    return await session.scalar(stmt)

async def get_access_rule_with_role(
        session: AsyncSession,
        access_rule_id: int,
) -> AccessRule | None:
    """
    Get access rule with role loaded.
    
    Args:
        session: Async database session
        access_rule_id: ID of rule to retrieve
        
    Returns:
        AccessRule | None: AccessRule object with role if found, None otherwise
    """
    stmt = (
        select(AccessRule)
        .where(AccessRule.id == access_rule_id)
        .options(joinedload(AccessRule.role))
    )
    return await session.scalar(stmt)