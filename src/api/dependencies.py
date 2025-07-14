from typing import Annotated

from annotated_types import Ge
from database.core import DBSession
import crud
import models
from exceptions.exceptions import NotFoundException

IDField = Annotated[int, Ge(1)]

async def get_user_by_id(
        sesison: DBSession,
        user_id: IDField,
) -> models.User:
    user = await crud.get_user(sesison, user_id)
    if not user:
        raise NotFoundException("User")
    return user

async def get_room_by_id(
        sesison: DBSession,
        room_id: IDField,
) -> models.Room:
    room = await crud.get_room(sesison, room_id)
    if not room:
        raise NotFoundException("Room")
    return room

async def get_role_by_id(
        session: DBSession,
        role_id: IDField
) -> models.Role:
    if role := await crud.get_role(session, role_id):
        return role
    else:
        raise NotFoundException("Role")
    
async def get_floor_by_id(
        session: DBSession,
        floor_id: IDField
) -> models.Floor:
    if floor := await crud.get_floor(session, floor_id):
        return floor
    else:
        raise NotFoundException("Floor")
    
async def get_current_presence_by_id(
        session: DBSession,
        current_presence_id: IDField,
) -> models.CurrentPresence:
    if current_presence := await crud.get_current_presence(session, current_presence_id):
        return current_presence
    else: 
        raise NotFoundException("Current presence record")
    
async def get_building_by_id(
        session: DBSession,
        building_id: IDField
) -> models.Building:
    if building := await crud.get_building(session, building_id):
        return building
    else:
        raise NotFoundException("Building")
    
async def get_access_rule_by_id(
        session: DBSession,
        access_rule_id: IDField,
) -> models.AccessRule:
    if access_rule := await crud.get_access_rule(session, access_rule_id):
        return access_rule
    else:
        raise NotFoundException("Access rule")
    
async def get_access_log_by_id(
        session: DBSession,
        access_log_id: IDField,
) -> models.AccessLog:
    if access_log := await crud.get_access_log(session, access_log_id):
        return access_log
    else:
        raise NotFoundException("Access log")