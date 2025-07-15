from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from src.crud import access_log as crud
from src.models import AccessLog
import src.schemas.access_log as schemas
from .dependencies import DBSession, get_access_log_by_id

router = APIRouter(prefix="/access-log", tags=["Access Logs"])

@router.post("/", response_model=schemas.AccessLogOut, status_code=status.HTTP_201_CREATED)
async def create_access_log(
    session: DBSession,
    access_log_in: schemas.AccessLogCreate,
): 
    return await crud.create_access_log(session, access_log_in)

@router.put("/{access_log_id}", response_model=schemas.AccessLogOut)
async def update_access_log(
    session: DBSession,
    access_log_in: schemas.AccessLogUpdate,
    access_log: AccessLog = Depends(get_access_log_by_id)
):
    return await crud.update_access_log(
        session, 
        access_log_in=access_log_in, 
        access_log=access_log
    )

@router.patch("/{access_log_id}", response_model=schemas.AccessLogOut)
async def update_access_log_partical(
    session: DBSession,
    access_log_in: schemas.AccessLogUpdatePartical,
    access_log: AccessLog = Depends(get_access_log_by_id)
):
    return await crud.update_access_log(
        session, 
        access_log_in=access_log_in, 
        access_log=access_log,
        partial=True,
    )

@router.delete("/{access_log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_access_log(
    session: DBSession,
    access_log: AccessLog = Depends(get_access_log_by_id)
): 
    await crud.delete_access_log(session, access_log)

@router.get("/", response_model=list[schemas.AccessLogOut])
async def get_access_logs(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100,
):
    access_logs = await crud.get_access_logs(session, offset, limit)
    return list(access_logs)

@router.get("/with-user", response_model=list[schemas.AccessLogWithUser])
async def get_access_logs_with_user(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100, 
):
    access_logs = await crud.get_access_logs_with_user(session, offset, limit)
    return list(access_logs)

@router.get("/with-room", response_model=list[schemas.AccessLogWithRoom])
async def get_access_logs_with_room(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100, 
):
    access_logs = await crud.get_access_logs_with_room(session, offset, limit)
    return list(access_logs)

@router.get("{access_log_id}", response_model=schemas.AccessLogOut)
async def get_access_log(
    access_log: AccessLog = Depends(get_access_log_by_id)
):
    return access_log


