from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from .auth_schemas import Token
from src.models import User
from src.schemas.user import UserOut
from src.crud.user import get_user_by_email
from .utils import (
    refresh_token_scheme,
    check_token_with_type,
    create_token,
    TokenType,
)
from .dependencies import DBSession
from .service import get_current_active_user, authenticate_user
from .exceptions import IncorectLoginData, InvalidCredentialsError

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post(
    "/token", 
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect login data"}
                }
            }
        }
    }
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DBSession) -> Token:
    user = await authenticate_user(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise IncorectLoginData
    
    payload: dict ={
            "sub": user.email,
        }
    
    access_token = create_token(payload=payload, token_type=TokenType.ACCESS,)
    refresh_token = create_token( payload=payload, token_type=TokenType.REFRESH,)

    return Token( 
        access_token=access_token, 
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh", 
    response_model_exclude_none=True,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid or expired refresh token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    })
async def refresh_token(    
    session: DBSession,
    credentials: HTTPAuthorizationCredentials = Depends(refresh_token_scheme),
) -> Token:
    if not credentials:
        raise exceptions.InvalidCredentialsError
    
    token_data = check_token_with_type(token=credentials.credentials, token_type=TokenType.REFRESH)
    user = await get_user_by_email(session, email=token_data.email)
    if not user:
        raise InvalidCredentialsError
    
    access_token = create_token(
        payload={
            "sub": user.email,
        },
        token_type=TokenType.ACCESS,
    )

    return Token(access_token=access_token)

@router.get(
    "/me", 
    response_model=UserOut,   
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid or missing access token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Inactive user",
            "content": {
                "application/json": {
                    "example": {"detail": "User is inactive"}
                }
            }
        }
    }
)
async def users_me(user: User = Depends(get_current_active_user)):
    return user