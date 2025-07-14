import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse

from core.config import settings
from api import api_router
from auth.controller import router as auth_router

main_app = FastAPI()
main_app.include_router(api_router)
main_app.include_router(auth_router)

@main_app.get(
    "/",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="""
This endpoint is used to verify that the API server is up and running.
It returns a simple plain text response `OK` if the service is healthy.
Useful for uptime monitoring, load balancers, or readiness/liveness probes.
""",
    response_description="Plain text response confirming the server is healthy (`OK`).",
)
async def health_check():
    return "OK"


if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
