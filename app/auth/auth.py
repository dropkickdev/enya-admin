from fastapi import Request
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase
# from authcontrol import Authcontrol
from .models.user import UserMod, User, UserCreate, UserUpdate, UserDB

from app.settings import settings as s


jwtauth = JWTAuthentication(secret=s.SECRET_KEY,
                            lifetime_seconds=s.ACCESS_TOKEN_EXPIRE)

user_db = TortoiseUserDatabase(UserDB, UserMod)
fapi_user = FastAPIUsers(user_db, [jwtauth], User, UserCreate, UserUpdate, UserDB) # noqa`

# authcon = Authcontrol(s, jwtauth, user_db, fapi_user)



async def signup_callback(user: UserDB, request: Request):      # noqa
    pass
    # Add groups to the new user
    # groups = await Group.filter(name__in=s.USER_GROUPS)
    # user = await UserTable.get(pk=user.id).only('id')
    # await user.groups.add(*groups)


async def user_callback(user: UserDB, updated_fields: dict, request: Request):      # noqa
    pass