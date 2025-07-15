from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from src.auth.service import get_current_active_admin_user
from src.crud import access_rule as crud
from src.models import AccessRule
import src.schemas.access_rule as schemas
from .dependencies import DBSession, get_access_rule_by_id

router = APIRouter(prefix="/access_rule", tags=["Access Rules"], dependencies=[Depends(get_current_active_admin_user)])

@router.post("/", response_model=schemas.AccessRuleOut, status_code=status.HTTP_201_CREATED)
async def create_access_rule(
    session: DBSession,
    access_rule_in: schemas.AccessRuleCreate,
):
    return await crud.create_access_rule(session, access_rule_in)

@router.put("/{access_rule_id}", response_model=schemas.AccessRuleOut)
async def update_accesss_rule(
    session: DBSession,
    access_rule_in: schemas.AccessRuleUpdate,
    access_rule: AccessRule = Depends(get_access_rule_by_id)
):
    return await crud.update_access_rule(
        session=session,
        access_rule_in=access_rule_in,
        access_rule=access_rule
    )

@router.put("/{access_rule_id}", response_model=schemas.AccessRuleOut)
async def update_accesss_rule_partical(
    session: DBSession,
    access_rule_in: schemas.AccessRuleUpdatePartical,
    access_rule: AccessRule = Depends(get_access_rule_by_id)
):
    return await crud.update_access_rule(
        session=session,
        access_rule_in=access_rule_in,
        access_rule=access_rule,
        partial=True,
    )

@router.delete("/{access_rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_access_rule(
    session: DBSession,
    access_rule: AccessRule = Depends(get_access_rule_by_id)
):
    await crud.delete_access_rule(session, access_rule)

@router.get("/", response_model=list[schemas.AccessRuleOut])
async def get_access_rules(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
): 
    access_rules = await crud.get_access_rules(session, offset, limit)
    return list(access_rules)

@router.get("/with-room", response_model=list[schemas.AccessRuleWithRoom])
async def get_access_rules_with_room(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
): 
    access_rules = await crud.get_access_rules_with_room(session, offset, limit)
    return list(access_rules)

@router.get("/with-role", response_model=list[schemas.AccessRuleWithRole])
async def get_access_rules_with_role(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
): 
    access_rules = await crud.get_access_rules_with_role(session, offset, limit)
    return list(access_rules)

@router.get("/{access_rule_id}", response_model=schemas.AccessRuleOut)
async def get_access_rule(
    access_rule: AccessRule = Depends(get_access_rule_by_id)
):
    return access_rule