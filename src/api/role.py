from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from database.core import DBSession
from crud import role as role_crud
from models import Role
import schemas.role as schemas
from .dependencies import get_role_by_id

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=schemas.RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    session: DBSession,
    role_in: schemas.RoleCreate,
):
    return await role_crud.create_role(session, role_in)

@router.put("/{role_id}", response_model=schemas.RoleOut)
async def update_role(
    session: DBSession,    
    role_in: schemas.RoleUpdate,
    role: Role = Depends(get_role_by_id),
):
    return await role_crud.update_role(session, role=role, role_in=role_in)

@router.patch("/{role_id}", response_model=schemas.RoleOut)
async def update_role_partical(
    session:DBSession,    
    role_in: schemas.RoleUpdatePartical,
    role: Role = Depends(get_role_by_id),
):
    return await role_crud.update_role(session, role=role, role_in=role_in, partical=True)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    session: DBSession,
    role: Role = Depends(get_role_by_id)
):
    await role_crud.delete_role(session, role)

@router.get("/", response_model=list[schemas.RoleOut])
async def get_roles(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100

):
    roles = await role_crud.get_roles(session, offset, limit)
    return list(roles)

@router.get("/with-access-rules", response_model=list[schemas.RoleWithAccessRules])
async def get_roles_with_access_rules(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100

):
    roles = await role_crud.get_roles_with_access_rules(session, offset, limit)
    return list(roles)

@router.get("/with-users", response_model=list[schemas.RoleWithUsers])
async def get_roles_with_users(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100

):
    roles = await role_crud.get_roles_with_users(session, offset, limit)
    return list(roles)


@router.get("/{role_id}", response_model=schemas.RoleOut)
async def get_role(
    role: Role = Depends(get_role_by_id)
):
    return role