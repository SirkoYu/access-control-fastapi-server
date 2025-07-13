from typing import Annotated

from annotated_types import Ge
from database.core import DBSession
from models import User
from crud.user import get_user
from exceptions.exceptions import UserNotFoundError

IDField = Annotated[int, Ge(1)]

async def get_user_by_id(
        sesison: DBSession,
        user_id: IDField,
) -> User:
    user = await get_user(sesison, user_id)
    if not user:
        raise UserNotFoundError
    return user