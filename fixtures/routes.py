import json, time, random
from fastapi import APIRouter, HTTPException, status, FastAPI
from fastapi_users.user import get_create_user
from starlette.testclient import TestClient
from tortoise import transactions
from fastapi_users.user import CreateUserProtocol, UserAlreadyExists
from fastapi_users.router.common import ErrorCode, run_handler
from tortoise.contrib.starlette import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr

from app import ic
from app.settings import settings as s
from app.settings.db import DATABASE
from app.auth import userdb, fapiuser, jwtauth, UserDB, UserCreate, UserMod
from app.auth.models.rbac import Group, Permission
from app.auth.models.core import Option
from tests.auth_test import VERIFIED_USER_DEMO



fixturerouter = APIRouter()
data_list = ['page', 'book']

app = FastAPI()     # noqa
# fapiuser.get_register_router(register_callback)
# register_tortoise(
#     app,
#     config=DATABASE,
#     generate_schemas=True,
# )
# origins = ['http://localhost:3000', 'http://127.0.0.1:3000']
# app.add_middleware(
#     CORSMiddleware, allow_origins=origins, allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# @fixturerouter.get('/init')
# async def fixtures():
#     try:
#         async with transactions.in_transaction():
#             # Groups
#             groups = []
#             for group in ['AdminGroup', 'StaffGroup',
#                           'AccountGroup', 'DataGroup',  # Default groups
#                           'StrictdataGroup']:
#                 groups.append(Group(name=group))
#             await Group.bulk_create(groups)
#
#             # Permissions
#             permissions = []
#             permissions.extend([
#                 Permission(name=f'Ban user', code=f'auth.ban'),
#                 Permission(name=f'Unban user', code=f'auth.unban'),
#                 Permission(name=f'Reset password counter', code=f'auth.reset_password_counter'),
#             ])
#             for i in ['user', 'settings', 'profile'] + data_list:
#                 permissions.extend([
#                     Permission(name=f'{i.capitalize()} Create', code=f'{i.lower()}.create'),
#                     Permission(name=f'{i.capitalize()} Read', code=f'{i.lower()}.read'),
#                     Permission(name=f'{i.capitalize()} Update', code=f'{i.lower()}.update'),
#                     Permission(name=f'{i.capitalize()} Delete', code=f'{i.lower()}.delete'),
#                     Permission(name=f'{i.capitalize()} Hard Delete', code=f'{i.lower()}.hard_delete'),
#                 ])
#             await Permission.bulk_create(permissions)
#
#             # Group permissions
#             await group_permissions(data_list)
#
#             # Create your first user here and populate VERIFIED_USER_ID
#
#             return True
#     except Exception:
#         return False

perms = {
    'AdminGroup': {
        'user': ['create', 'delete', 'hard_delete'],
        'auth': ['ban', 'unban', 'reset_password_counter'],
    },
    'StaffGroup': {
        'auth': ['ban', 'unban', 'reset_password_counter'],
    },
    'DataGroup': {
        'page': ['create', 'read', 'update', 'delete'],
        'book': ['create', 'read', 'update', 'delete'],
    },
    'AccountGroup': {
        'profile': ['read', 'update'],
        'setting': ['read', 'update'],
    },
}


@fixturerouter.get('/init', summary="Groups, Permissions, and relationships")
async def create_groups_permissions():
    try:
        permlist = []
        for groupname, val in perms.items():
            group = await Group.create(name=groupname)
            for app, actions in val.items():
                for i in actions:
                    code = f'{app}.{i}'
                    if code  in permlist:
                        continue
                    await Permission.create(
                        name=f'{app.capitalize()} {i.capitalize()}', code=code
                    )
                    permlist.append(code)
    
        for groupname, val in perms.items():
            group = await Group.get(name=groupname).only('id')
            ll = []
            for app, actions in val.items():
                for i in actions:
                    ll.append(f'{app}.{i}')
            permlist = await Permission.filter(code__in=ll).only('id')
            await group.permissions.add(*permlist)
        return True
    except Exception:
        return False


@fixturerouter.get('/users', summary="Create users")
async def create_users():
    try:
        usserdata = UserCreate(email=EmailStr('enchance@gmail.com'), password='pass123')
        create_user = get_create_user(userdb, UserDB)
        created_user = await create_user(usserdata, safe=True)
        ret = created_user
        groups = await Group.filter(name__in=s.USER_GROUPS)
        user = await UserMod.get(pk=created_user.id)
        user.is_verified = True
        user.is_superuser = True
        await user.save()
        await user.groups.add(*groups)

        usserdata = UserCreate(email=EmailStr('unverified@gmail.com'), password='pass123')
        create_user = get_create_user(userdb, UserDB)
        created_user = await create_user(usserdata, safe=True)
        groups = await Group.filter(name__in=s.USER_GROUPS)
        user = await UserMod.get(pk=created_user.id)
        await user.groups.add(*groups)
        
        return ret
    
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )


@fixturerouter.get('/options', summary='Don\'t run if you haven\'t created users yet')
async def create_options():
    try:
        await Option.create(name='sitename', value='Feather Admin')
        await Option.create(name='author', value='DropkickDev')
        await Option.create(name='cool', value='yo', user_id=VERIFIED_USER_DEMO)
        await Option.create(name='theme', value='purple', user_id=VERIFIED_USER_DEMO)
        return True
    except Exception:
        return False
    
# @router.get('/testing')
# async def testing():
#     try:
#         # rtoken = await Token.filter(id__in=[1,2]).update(is_blacklisted=False)
#         rtoken = await Token.get(id=1).only('id')
#         rtoken.is_blacklisted=True
#         await rtoken.save(update_fields=['is_blacklisted'])
#         return rtoken
#     except DoesNotExist:
#         return False

