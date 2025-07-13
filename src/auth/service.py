from typing import Annotated

from fastapi import Depends, HTTPException, status

from .utils import verify_password, check_token_with_type, TokenType, oauth2_scheme
from schemas.user import UserOut
from database.core import DBSession
from crud.user import get_user_by_email
from exceptions import exceptions

from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: DBSession):
    token_data = check_token_with_type(token=token, token_type=TokenType.ACCESS)
    
    user = await get_user_by_email(session=session, email=token_data.email) # type: ignore
    if user is None:
        raise exceptions.InvalidCredentialsError
    return user

async def authenticate_user(session: AsyncSession, email: str, password: str):
    user = await get_user_by_email(session=session, email=email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_active_user(current_user: Annotated[UserOut, Depends(get_current_user)]):
    if not current_user.is_active:
        raise exceptions.InactiveUserError(user_id=current_user.id)
    return current_user