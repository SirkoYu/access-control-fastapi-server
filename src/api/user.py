from typing import Annotated
from annotated_types import Ge

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from crud import user as user_crud
from exceptions.exceptions import UserNotFoundError
from database.core import DBSession
from models import User
from schemas.user import (
    UserCreate,
    UserUpdate,
    UserUpdatePatrical,
    UserOut,
    UserWithRoles,
    UserWithCurrentPresence,
    UserWithAccessLogs
)
from .dependepcies import get_user_by_id, IDField

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(    
    user_in: UserCreate,
    session: DBSession,
):
    return await user_crud.create_user(user_in=user_in, session=session)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    session: DBSession,
    user_in: UserUpdate,
    user: User = Depends(get_user_by_id),
):
    return await user_crud.update_user(session, user_in, user)
    
@router.patch("/{user_id}", response_model=UserOut)
async def update_user_partical(
    session: DBSession,
    user_in: UserUpdatePatrical,
    user: User = Depends(get_user_by_id),
):
    return await user_crud.update_user(session, user_in, user, partical=True)
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(    
    session: DBSession,
    user: User = Depends(get_user_by_id),
):
    await user_crud.delete_user(session, user)

@router.get("/", response_model=list[UserOut])
async def get_users(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    users = await user_crud.get_users(session, offset, limit)
    return list(users)

@router.get("/user-with-roles/{user_id}", response_model=UserWithRoles)
async def get_user_with_roles(
    session: DBSession,
    user_id: IDField
):
    user = await user_crud.get_user_with_roles(session, user_id)
    if not user:
        raise UserNotFoundError
    return user

@router.get("/user-with-current-presence/{user_id}", response_model=UserWithCurrentPresence)
async def get_user_with_current_presence(
    session: DBSession,
    user_id: IDField
):
    user = await user_crud.get_user_with_current_presence(session, user_id)
    if not user:
        raise UserNotFoundError
    return user

@router.get("/user-with-access_logs/{user_id}", response_model=UserWithAccessLogs)
async def get_user_with_access_logs(
    session: DBSession,
    user_id: IDField
):
    user = await user_crud.get_user_with_accesslogs(session, user_id)
    if not user:
        raise UserNotFoundError
    return user

@router.get("/users-with-roles", response_model=list[UserWithRoles])
async def get_users_with_roles(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    users = await user_crud.get_users_with_roles(session, offset, limit)
    return users

@router.get("/users-with-current-presence", response_model=list[UserWithCurrentPresence])
async def get_users_with_current_presence(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    users = await user_crud.get_users_with_current_presence(session, offset, limit)
    return users

@router.get("/users-with-access_logs", response_model=list[UserWithAccessLogs])
async def get_users_with_access_logs(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    users = await user_crud.get_users_with_access_logs(session, offset, limit)
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user_with_id(
    user: User = Depends(get_user_by_id)
):
    return user