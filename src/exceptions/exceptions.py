from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, entity: str = "Entity", entity_id: int|None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} not found" if entity_id is None else f"{entity} with id={entity_id} not found"
        )

class AuthError(HTTPException):
    pass

class InvalidCredentialsError(AuthError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials", 
            headers={"WWW-Authenticate": "Bearer"},
        )

class IncorectLoginData(AuthError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UserError(HTTPException):
    pass


class UserNotFoundError(UserError):
    def __init__(self, user_id: int|None = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found" if user_id is None else f"User with {user_id!r} not found",
        )

class InactiveUserError(UserError):
    def __init__(self, user_id: int| None = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive" if user_id is None else f"User with {user_id} is inactive"
        )