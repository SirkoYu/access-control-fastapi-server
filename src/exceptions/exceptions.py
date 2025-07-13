from fastapi import HTTPException, status


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
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User not found",
        )

class InactiveUserError(UserError):
    def __init__(self, user_id: int| None = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is inactive" if user_id is None else f"User with {user_id} is inactive"
        )