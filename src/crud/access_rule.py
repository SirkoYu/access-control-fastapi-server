from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models import AccessRule
from schemas.access_rule import (
    AccessRuleCreate,
    AccessRuleUpdate,
    AccessRuleUpdatePartical,
)

async def create_access_rule(
        session: AsyncSession,
        access_rule_in: AccessRuleCreate,
) -> AccessRule:
    access_rule = AccessRule(**access_rule_in.model_dump())
    session.add(access_rule)
    await session.commit()
    await session.refresh(access_rule)

    return access_rule

async def update_access_rule(
        session: AsyncSession,
        access_rule: AccessRule,
        access_rule_in: AccessRuleUpdate|AccessRuleUpdatePartical,
        partical: bool = False,
) -> AccessRule:
    for name, value in access_rule_in.model_dump(exclude_none=partical).items():
        setattr(access_rule, name, value)
    await session.commit()
    await session.refresh(access_rule)

    return access_rule

async def delete_access_rule(
        session: AsyncSession,
        access_rule: AccessRule,
) -> None:
    await session.delete(access_rule)
    await session.commit()

async def get_access_rule(
        session: AsyncSession,
        access_rule_id: int
) -> AccessRule|None:
    return await session.get(AccessRule, access_rule_id)

async def get_access_rules(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    stmt = (
        select(AccessRule)
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(AccessRule.id)
    )

    access_rules = await session.scalars(statement=stmt)
    return access_rules.all()

async def get_access_rules_with_room(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    stmt = (
        select(AccessRule)
        .options(joinedload(AccessRule.room))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(AccessRule.id)
    )

    access_rules = await session.scalars(statement=stmt)
    return access_rules.all()

async def get_access_rules_with_role(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> Sequence[AccessRule]:
    stmt = (
        select(AccessRule)
        .options(joinedload(AccessRule.role))
        .offset(offset=offset)
        .limit(limit=limit)
        .order_by(AccessRule.id)
    )

    access_rules = await session.scalars(statement=stmt)
    return access_rules.all()

async def get_access_rule_with_room(
        session: AsyncSession,
        access_rule_id: int,
) -> AccessRule|None:
    stmt = (
        select(AccessRule)
        .where(AccessRule.id == access_rule_id)
        .options(joinedload(AccessRule.room))
    )
    return await session.scalar(statement=stmt)

async def get_access_rule_with_role(
        session: AsyncSession,
        access_rule_id: int,
) -> AccessRule|None:
    stmt = (
        select(AccessRule)
        .where(AccessRule.id == access_rule_id)
        .options(joinedload(AccessRule.role))
    )
    return await session.scalar(statement=stmt)