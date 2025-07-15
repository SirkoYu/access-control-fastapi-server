from typing import Annotated
from annotated_types import Ge

from fastapi import Depends, APIRouter, status

from src.auth.service import get_current_active_admin_user
from src.crud import room as room_crud
from src.models import Room
import src.schemas.room as schemas
from .dependencies import DBSession, IDField, get_room_by_id

router = APIRouter(prefix="/rooms", tags=["Rooms"], dependencies=[Depends(get_current_active_admin_user)])

@router.post("/", response_model=schemas.RoomOut, status_code=status.HTTP_201_CREATED)
async def create_room_(
    session: DBSession, 
    room_in: schemas.RoomCreate
):
    return await room_crud.create_room(session, room_in)

@router.put("/{room_id}", response_model=schemas.RoomOut)
async def update_room(
    session: DBSession,
    room_in: schemas.RoomUpdate,
    room: Room = Depends(get_room_by_id),
):
    return await room_crud.update_room(session, room, room_in)

@router.patch("/{room_id}", response_model=schemas.RoomOut)
async def update_room_partical(
    session: DBSession,
    room_in: schemas.RoomUpdatePartical,
    room: Room = Depends(get_room_by_id),
):
    return await room_crud.update_room(session, room, room_in, partial=True)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    session: DBSession,
    room: Room = Depends(get_room_by_id)
):
    await room_crud.delete_room(session, room)

@router.get("/with-floor", response_model=list[schemas.RoomWithFloor])
async def get_rooms_with_floors(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    rooms = await room_crud.get_rooms_with_floor(session, offset, limit)
    return list(rooms)

@router.get("/with-access-rules", response_model=list[schemas.RoomWithAccessRules])
async def get_rooms_with_access_rules(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    rooms = await room_crud.get_rooms_with_access_rules(session, offset, limit)
    return list(rooms)

@router.get("/with-access-logs", response_model=list[schemas.RoomWithAccessLogs])
async def get_rooms_with_access_logs(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    rooms = await room_crud.get_rooms_with_access_logs(session, offset, limit)
    return list(rooms)

@router.get("/with-current-presence", response_model=list[schemas.RoomWithCurrentPresence])
async def get_rooms_with_current_presence(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
):
    rooms = await room_crud.get_rooms_with_current_presence(session, offset, limit)
    return list(rooms)

@router.get("/", response_model=list[schemas.RoomOut])
async def get_rooms(
    session: DBSession,
    offset: Annotated[int, Ge(0)] = 0,
    limit: Annotated[int, Ge(1)] = 100
): 
    rooms = await room_crud.get_rooms(session, offset, limit)
    return list(rooms)

@router.get("/{room_id}", response_model=schemas.RoomOut)
async def get_room(
    session: DBSession,
    room_id: IDField,
):
    return await room_crud.get_room(session, room_id)