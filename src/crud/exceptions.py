from typing import Any

from fastapi import status

from src.exceptions.exceptions import AppException

class CrudException(AppException):
    """Base exception for all CRUD operations."""
    def __init__(
        self,
        model_name: str,
        detail: str,
        message: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        original_exc: Exception | None = None,
        log_error: bool = True,
    ):
        super().__init__(
            detail=detail,
            message=message,
            status_code=status_code,
            original_exc=original_exc,
            log_error=log_error
        )


class EntityNotFoundException(AppException):
    """Raised when entity is not found."""
    def __init__(
        self,
        model_name: str,        
        detail: str|None = None,
        entity_id: Any = None,
        log_error: bool = False
    ):
        if detail is None:
            detail = (
                f"{model_name} not found" 
                if entity_id is None 
                else f"{model_name} with id={entity_id} not found"
            )
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            log_error=log_error
        )


class AlreadyExistsException(CrudException):
    """Raised when entity already exists (unique constraint violation)."""
    def __init__(
        self,
        model_name: str,
        field_name: str|None = None,
        field_value: Any = None,
        status_code: int = status.HTTP_409_CONFLICT,
        log_error: bool = False
    ):
        super().__init__(
            model_name=model_name,
            detail=f"{model_name} with {field_name}={field_value} already exists" if field_name is not None else f"{model_name} with this fields already exists",
            status_code=status_code,
            log_error=log_error
        )


class CreateException(CrudException):
    """Raised when entity creation fails."""
    def __init__(
        self,
        model_name: str,
        original_exc: Exception | None = None
    ):
        super().__init__(
            model_name=model_name,
            detail=f"Failed to create {model_name}",
            original_exc=original_exc
        )


class UpdateException(CrudException):
    """Raised when entity update fails."""
    def __init__(
        self,
        model_name: str,
        entity_id: Any,
        original_exc: Exception | None = None
    ):
        super().__init__(
            model_name=model_name,
            detail=f"Failed to update {model_name} with id={entity_id}",
            original_exc=original_exc
        )


class DeleteException(CrudException):
    """Raised when entity deletion fails."""
    def __init__(
        self,
        model_name: str,
        entity_id: Any,
        original_exc: Exception | None = None
    ):
        super().__init__(
            model_name=model_name,
            detail=f"Failed to delete {model_name} with id={entity_id}",
            original_exc=original_exc
        )

class UserAlreadyExistsException(AlreadyExistsException):
    """Specialized exception for user conflicts."""
    def __init__(self, email: str):
        super().__init__(
            model_name="User",
            field_name="email",
            field_value=email
        )