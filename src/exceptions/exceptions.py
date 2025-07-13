from fastapi import HTTPException, status

class InvalidCredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials", 
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