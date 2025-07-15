"""
CRUD operations for User model with comprehensive error handling.
"""

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from pydantic import EmailStr

from src.auth.utils import hash_password
from src.models import User
from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserUpdatePatrical,
)
import src.crud.exceptions as exceptions

async def create_user(
        user_in: UserCreate, 
        session: AsyncSession
) -> User:
    """
    Create a new user in the database.
    
    Args:
        user_in: UserCreate schema with user data
        session: Async database session
        
    Returns:
        User: Newly created User object
        
    Raises:
        UserAlreadyExistsException: If user with same email already exists
        CreateException: If general creation error occurs
    """
    try:
        user = User(**user_in.model_dump(exclude={"password"}))
        user.password_hash = hash_password(user_in.password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError as e:
        await session.rollback()
        if "email" in str(e).lower():
            raise exceptions.UserAlreadyExistsException(email=user_in.email) from e
        raise exceptions.CreateException(model_name="User", original_exc=e) from e
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.CreateException(model_name="User", original_exc=e) from e


async def update_user(
        session: AsyncSession,
        user_in: UserUpdate | UserUpdatePatrical,
        user: User,
        partial: bool = False,
) -> User:
    """
    Update existing user data.
    
    Args:
        session: Async database session
        user_in: Update data (full or partial)
        user: User object to update
        partial: Whether to perform partial update
        
    Returns:
        User: Updated User object
        
    Raises:
        UpdateException: If update operation fails
    """
    try:
        for name, value in user_in.model_dump(exclude_none=partial).items():
            if name == "password":
                name = "password_hash"
                value = hash_password(value)
            setattr(user, name, value)
        await session.commit()
        await session.refresh(user)
        return user
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.UpdateException(
            model_name="User",
            entity_id=user.id,
            original_exc=e
        ) from e


async def delete_user(
        session: AsyncSession, 
        user: User
) -> None:
    """
    Delete user from database.
    
    Args:
        session: Async database session
        user: User object to delete
        
    Raises:
        DeleteException: If deletion fails
    """
    try:
        await session.delete(user)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise exceptions.DeleteException(
            model_name="User",
            entity_id=user.id,
            original_exc=e
        ) from e


async def get_user(
        session: AsyncSession, 
        user_id: int
) -> User | None:
    """
    Get user by ID.
    
    Args:
        session: Async database session
        user_id: ID of user to retrieve
        
    Returns:
        User | None: User object if found, None otherwise
    """
    return await session.get(User, user_id)


async def get_users(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    """
    Get paginated list of users.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of users to return
        
    Returns:
        Sequence[User]: List of User objects
    """
    stmt = (
        select(User)
        .offset(offset)
        .limit(limit)
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    return users.all()


async def get_user_with_roles(
        session: AsyncSession,
        user_id: int,
) -> User | None:
    """
    Get user with their roles loaded.
    
    Args:
        session: Async database session
        user_id: ID of user to retrieve
        
    Returns:
        User | None: User object with roles if found, None otherwise
    """
    stmt = select(User).where(User.id == user_id).options(selectinload(User.roles))
    return await session.scalar(stmt)


async def get_user_with_accesslogs(
        session: AsyncSession,
        user_id: int,
) -> User | None:
    """
    Get user with their access logs loaded.
    
    Args:
        session: Async database session
        user_id: ID of user to retrieve
        
    Returns:
        User | None: User object with access logs if found, None otherwise
    """
    stmt = select(User).where(User.id == user_id).options(selectinload(User.access_logs))
    return await session.scalar(stmt)


async def get_user_with_current_presence(
        session: AsyncSession,
        user_id: int
) -> User | None:
    """
    Get user with their current presence loaded.
    
    Args:
        session: Async database session
        user_id: ID of user to retrieve
        
    Returns:
        User | None: User object with current presence if found, None otherwise
    """
    stmt = select(User).where(User.id == user_id).options(joinedload(User.current_presence))
    return await session.scalar(stmt)


async def get_users_with_roles(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    """
    Get paginated list of users with their roles loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of users to return
        
    Returns:
        Sequence[User]: List of User objects with roles
    """
    stmt = (
        select(User)
        .options(selectinload(User.roles))
        .offset(offset)
        .limit(limit)
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    return users.all()


async def get_users_with_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    """
    Get paginated list of users with their access logs loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of users to return
        
    Returns:
        Sequence[User]: List of User objects with access logs
    """
    stmt = (
        select(User)
        .options(selectinload(User.access_logs))
        .offset(offset)
        .limit(limit)
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    return users.all()


async def get_users_with_current_presence(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    """
    Get paginated list of users with their current presence loaded.
    
    Args:
        session: Async database session
        offset: Pagination offset
        limit: Maximum number of users to return
        
    Returns:
        Sequence[User]: List of User objects with current presence
    """
    stmt = (
        select(User)
        .options(joinedload(User.current_presence))
        .offset(offset)
        .limit(limit)
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    return users.all()


async def get_user_by_email(
        session: AsyncSession,
        email: EmailStr,
) -> User | None:
    """
    Get user by email address.
    
    Args:
        session: Async database session
        email: Email address to search for
        
    Returns:
        User | None: User object if found, None otherwise
    """
    stmt = select(User).where(User.email == email)
    return await session.scalar(stmt)