from fastapi import status

class AppException(Exception):
    def __init__(
        self,        
        detail: str,
        message: str|None = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        original_exc: Exception|None = None,
        log_error: bool = True,
    ):
        self.message = (message or detail) if original_exc is None else str(original_exc)
        self.detail = detail
        self.status_code = status_code
        self.original_exc = original_exc
        self.log_error = log_error

        super().__init__(message)

        if original_exc:
            self.__cause__ = original_exc


class NotFoundException(AppException):
    def __init__(self, entity: str = "", entity_id: int|None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} not found" if entity_id is None else f"{entity} with id={entity_id} not found",
            log_error=False,
        )

