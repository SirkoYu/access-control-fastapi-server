from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from .auth_schemas import Token
from database.core import DBSession
from models import User
from schemas.user import UserOut
from crud.user import get_user_by_email
from .utils import (
    refresh_token_scheme,
    check_token_with_type,
    create_token,
    TokenType,
)
from .service import get_current_active_user, authenticate_user
from exceptions import exceptions

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DBSession) -> Token:
    user = await authenticate_user(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise exceptions.IncorectLoginData
    
    payload: dict ={
            "sub": user.email,
        }
    
    access_token = create_token(payload=payload, token_type=TokenType.ACCESS,)
    refresh_token = create_token( payload=payload, token_type=TokenType.REFRESH,)

    return Token( 
        access_token=access_token, 
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_token(    
    session: DBSession,
    credentials: HTTPAuthorizationCredentials = Depends(refresh_token_scheme),
) -> Token:
    if not credentials:
        raise exceptions.InvalidCredentialsError
    
    token_data = check_token_with_type(token=credentials.credentials, token_type=TokenType.REFRESH)
    user = await get_user_by_email(session, email=token_data.email)
    if not user:
        raise exceptions.InvalidCredentialsError
    
    access_token = create_token(
        payload={
            "sub": user.email,
        },
        token_type=TokenType.ACCESS,
    )

    return Token(access_token=access_token)

@router.get("/me", response_model=UserOut)
async def users_me(user: User = Depends(get_current_active_user)):
    return user