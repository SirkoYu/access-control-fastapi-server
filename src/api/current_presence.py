from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from database.core import DBSession
from crud import current_presence as crud
from models import CurrentPresence
import schemas.current_presence as schemas  
from .dependencies import get_current_presence_by_id

router = APIRouter(prefix="/current_presence", tags=["Current Presence"])

router.post("/", response_model=schemas.CurrentPresenceOut, status_code=status.HTTP_201_CREATED)
async def create_current_presence(
        session: DBSession,
        current_presence_in: schemas.CurrentPresenceCreate,
):
    return await crud.create_current_presence(session, current_presence_in)

@router.put("/{current_presence_id}", response_model=schemas.CurrentPresenceOut)
async def update_current_presence(
    session: DBSession,
    current_presence_in: schemas.CurrentPresenceUpdate,
    current_presence: CurrentPresence = Depends(get_current_presence_by_id)
):
    return await crud.update_current_presence(
        session=session, 
        current_presence_in=current_presence_in, 
        current_presence=current_presence
    )

@router.patch("/{current_presence_id}", response_model=schemas.CurrentPresenceOut)
async def update_current_presence_partical(
    session: DBSession,
    current_presence_in: schemas.CurrentPresenceUpdatePartical,
    current_presence: CurrentPresence = Depends(get_current_presence_by_id)
):
    return await crud.update_current_presence(
        session=session, 
        current_presence_in=current_presence_in, 
        current_presence=current_presence,
        partical=True,
    )

@router.delete("/{current_presence_id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_current_presence(
    sessiom: DBSession,
    current_presence: CurrentPresence = Depends(get_current_presence_by_id)
):
    await crud.delete_current_presence(sessiom, current_presence)

@router.get("/", response_model=list[schemas.CurrentPresenceOut])
async def get_current_presence_all(
    session: DBSession,
    offset: Annotated[int, Ge(0)],
    limit: Annotated[int, Ge(1)],
):
    result = await crud.get_current_presences(session, offset, limit)
    return list(result)

@router.get("/with-room", response_model=list[schemas.CurrentPresenceWithRoom])
async def get_current_presence_all_with_room(
    session: DBSession,
    offset: Annotated[int, Ge(0)],
    limit: Annotated[int, Ge(1)],
):
    result = await crud.get_current_presences_with_room(session, offset, limit)
    return list(result)

@router.get("/with-user", response_model=list[schemas.CurrentPresenceWithUser])
async def get_current_presence_all_with_user(
    session: DBSession,
    offset: Annotated[int, Ge(0)],
    limit: Annotated[int, Ge(1)],
):
    result = await crud.get_current_presences_with_user(session, offset, limit)
    return list(result)

@router.get("/{current_presence_id}", response_model=schemas.CurrentPresenceOut)
async def get_current_presence(
    current_presence: CurrentPresence = Depends(get_current_presence_by_id)
):
    return current_presence
