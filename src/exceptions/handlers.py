import logging

from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.requests import Request
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions.exceptions import AppException

logger = logging.getLogger("MainApp")

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        orig = exc.original_exc or exc.__cause__ or exc.__context__
        if exc.log_error:
            logger.error("%s\t%s\tError: %s", request.method, request.url.path, exc.message, exc_info=orig)
        
        response_class = PlainTextResponse if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR else JSONResponse

        return response_class(
            content=exc.detail,
            status_code=exc.status_code,
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def database_error_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error("Database error at '%s %s'\nError: %s:", request.method, request.url.path, str(exc), exc_info=exc)
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error"
        )
    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exc: Exception):
        logger.error("Unexpected error  at '%s %s':", request.method, request.url.path, exc_info=exc)
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )