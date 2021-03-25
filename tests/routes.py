from fastapi import Response, APIRouter, Depends, Body
from tortoise.exceptions import DoesNotExist

from app import ic
from app.auth import (
    TokenMod, Authcontrol, Authutils, jwtauth,
    current_user, UserMod, userdb,
    UserDB, UserDBComplete
)
from .auth_test import VERIFIED_USER_ID, VERIFIED_EMAIL_DEMO


testrouter = APIRouter()


@testrouter.post('/dev_view_user_data')
async def dev_view_user_data(response: Response, user=Depends(current_user)):
    # ic(user.permissions)
    # ic(type(user), user)
    # x = await UserMod.get(id=user.id).only('id', 'username', 'first_name', 'last_name')
    # ret = await x.add_perm(['profile.create', 'profile.read'])
    # ic(ret)
    return user


@testrouter.post('/dev_user_add_perm')
async def dev_add_perm(response: Response, user=Depends(current_user)):
    user = await UserMod.get(id=user.id).only('id', 'email')
    await user.add_perm('user.read')
    await user.add_perm(['user.delete', 'user.update'])
    
    user_dict = await user.to_dict()
    user = UserDBComplete(**user_dict)
    return user


@testrouter.post('/dev_user_add_group')
async def dev_add_group(response: Response, user=Depends(current_user)):
    user = await UserMod.get(id=user.id).only('id', 'email')
    await user.add_group('StaffGroup')
    await user.add_group(['AdminGroup', 'StrictdataGroup'])
    
    user_dict = await user.to_dict()
    user = UserDBComplete(**user_dict)
    return user


@testrouter.post('/dev_token')
async def new_access_token(response: Response):
    """
    Modified '/auth/token' route from app.auth.routes. Highly modified. Not a good reference.
    """
    
    # FOR TESTING ONLY
    REFRESH_TOKEN_KEY = 'refresh_token'
    token = await TokenMod.get(author_id=VERIFIED_USER_ID)
    refresh_token = token.token
    
    try:
        # if refresh_token is None:
        #     raise Exception

        # token = await TokenMod.get(token=refresh_token, is_blacklisted=False) \
        #     .only('id', 'token', 'expires', 'author_id')
        user = await userdb.get(token.author_id)    # noqa

        mins = Authutils.expires(token.expires)
        # ic(mins)
        test_message = 'STILL OK'
        if mins <= 0:
            raise Exception
        elif mins <= 60:
            test_message = 'REFRESH ANYWAY'
            # refresh the refresh_token anyway before it expires
            try:
                token = await Authcontrol.update_refresh_token(user, token=token)
            except DoesNotExist:
                token = await Authcontrol.create_refresh_token(user)

            cookie = Authcontrol.refresh_cookie(REFRESH_TOKEN_KEY, token)
            # response.set_cookie(**cookie)

        ic(test_message)
        return await jwtauth.get_login_response(user, response)

    except (DoesNotExist, Exception) as e:
        test_message = 'EXPIRED'
        ic(test_message)
        # del response.headers['authorization']
        # response.delete_cookie(REFRESH_TOKEN_KEY)
        return dict(access_token='')