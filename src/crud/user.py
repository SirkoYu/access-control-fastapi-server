'''
CRUD opreations for User model.
'''

from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from pydantic import EmailStr
from auth.utils import hash_password

from src.auth.utils import hash_password
from src.models import User
from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserUpdatePatrical,
)

async def create_user(
        user_in: UserCreate, 
        session: AsyncSession
) -> User:
    user = User(**user_in.model_dump(exclude={"password"}))
    user.password_hash = hash_password(user_in.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_user(
        session: AsyncSession,
        user_in: UserUpdate|UserUpdatePatrical,
        user: User,
        partical: bool = False,
) -> User:
    for name, value in user_in.model_dump(exclude_none=partical).items():
        if name == "password":
            name = "password_hash"
            value = hash_password(value)
        setattr(user, name, value)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(
        session: AsyncSession, 
        user: User
) -> None:
    await session.delete(user)
    await session.commit()

async def get_user(
        session: AsyncSession, 
        user_id: int
) -> User|None:
    return await session.get(User, user_id)

async def get_users(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    stmt = (
        select(User)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(User.id)
    )
    users = await session.scalars(statement=stmt)
    return users.all()

async def get_user_with_roles(
        session: AsyncSession,
        user_id: int,
) -> User|None:
    stmt = select(User).where(User.id == user_id).options(selectinload(User.roles))
    user = await session.scalar(statement=stmt)
    return user

async def get_user_with_accesslogs(
        session: AsyncSession,
        user_id: int,
) -> User|None:
    stmt = select(User).where(User.id == user_id).options(selectinload(User.access_logs))
    user = await session.scalar(statement=stmt)
    return user

async def get_user_with_current_presence(
        session: AsyncSession,
        user_id: int
) -> User|None:
    stmt = select(User).where(User.id == user_id).options(joinedload(User.current_presence))
    user = await session.scalar(statement=stmt)
    return user

async def get_users_with_roles(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    stmt = (
        select(User)
        .options(selectinload(User.roles))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(User.id)
    )
    users = await session.scalars(statement=stmt)
    return users.all()

async def get_users_with_access_logs(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    stmt = (
        select(User)
        .options(selectinload(User.access_logs))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(User.id)
    )
    users = await session.scalars(statement=stmt)
    return users.all()

async def get_users_with_current_presence(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[User]:
    stmt = (
        select(User)
        .options(joinedload(User.current_presence))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(User.id)
    )
    users = await session.scalars(statement=stmt)
    return users.all()

async def get_user_by_email(
        session: AsyncSession,
        email: EmailStr,
) -> User|None:
    stmt = (
        select(User).
        where(User.email == email)
    )

    return await session.scalar(stmt)
