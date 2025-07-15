from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models import Role
from src.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleUpdatePartical,
)

async def create_role(
        session: AsyncSession, 
        role_in: RoleCreate
) -> Role:
    role = Role(**role_in.model_dump())
    session.add(role)
    await session.commit()
    await session.refresh(role)
    
    return role

async def update_role(
        session: AsyncSession,
        role: Role,
        role_in: RoleUpdate|RoleUpdatePartical,
        partical: bool = False,
) -> Role:
    for name, value in role_in.model_dump(exclude_none=partical).items():
        setattr(role, name, value)
    await session.commit()
    await session.refresh(role)
    return role

async def delete_role(
        session: AsyncSession, 
        role: Role
) -> None:
    await session.delete(role)
    await session.commit()

async def get_role(
        session: AsyncSession, 
        role_id: int
) -> Role|None:
    role = await session.get(Role, role_id)
    return role

async def get_roles(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Role]:
    stmt = (
        select(Role)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(statement=stmt)
    return roles.all()

async def get_role_with_access_rules(
        session: AsyncSession,
        role_id: int
) -> Role|None:
    stmt = (
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.access_rules))
    )
    return await session.scalar(stmt)

async def get_role_with_users(
        session: AsyncSession,
        role_id: int
) -> Role|None:
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
    stmt = (
        select(Role)
        .options(selectinload(Role.access_rules))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(stmt)
    return roles.all()

async def get_roles_with_users(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[Role]:
    stmt = (
        select(Role)
        .options(selectinload(Role.users))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(Role.id)
    )
    roles = await session.scalars(stmt)
    return roles.all()