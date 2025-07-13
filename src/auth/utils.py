from datetime import datetime, timedelta, timezone
import enum

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import ValidationError
import jwt
import bcrypt

from .auth_schemas import TokenData
from exceptions.exceptions import InvalidCredentialsError
from core.config import settings


class TokenType(enum.StrEnum):
    STR = "type"
    ACCESS = "access"
    REFRESH = "refresh"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
refresh_token_scheme = HTTPBearer(auto_error=False)


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.private_path.read_text(),
        algorithm: str = settings.auth.algorithm,
        expire_timedelta: timedelta| None = None,
        expire_minutes: int = settings.auth.token_expire_minutes,
):
    to_endode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_endode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
    return encoded

def decode_jwt(
        token: str|bytes,
        public_key: str = settings.auth.public_path.read_text(),
        algorithm: str = settings.auth.algorithm
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=algorithm)

    return decoded

def hash_password(password: str) -> str:
    hashed_password: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())

def create_token(
    token_type: str,
    payload: dict,
    private_key: str = settings.auth.private_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth.token_expire_minutes
)-> str:
    to_encode = payload.copy()
    to_encode.update({TokenType.STR : token_type})
    token = encode_jwt(
        payload=to_encode,
        private_key=private_key,
        algorithm=algorithm,
        expire_timedelta=expire_timedelta,
        expire_minutes=expire_minutes
        )
    
    return token


def check_token_with_type(token: str, token_type: str):
    try:
        payload = decode_jwt(token)

        token_data = TokenData(email=payload.get("sub"), type=payload.get("type"))

        if token_data.type != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type: {token_data.type!r} expected {token_type!r}"
            )
        
        return token_data

    except (jwt.InvalidTokenError, ValidationError):
        raise InvalidCredentialsError