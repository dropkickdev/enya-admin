from fastapi import Request, Depends, Body, APIRouter, status, HTTPException, Response, exceptions
from tortoise.exceptions import BaseORMException, DoesNotExist
from redis.exceptions import RedisError

from app import ic, red, exceptions as x
from app.settings import settings as s
from app.authentication import current_user, Group
from . import UserGroupPy, UserMod            # noqa
from ..pydantic import UpdateGroupPyd, CreateGroupPyd

grouprouter = APIRouter()

@grouprouter.post('', summary='Create a new Group')
async def create_group(res: Response, group: CreateGroupPyd, user=Depends(current_user)):
    if not await user.has_perm('group.create'):
        raise x.PermissionDenied()
    try:
        usermod = await UserMod.get_or_none(email=user.email).only('id')
        if not usermod:
            raise x.NotFoundError('User')
        
        if not await Group.exists(name=group.name):
            group = await Group.create(**group.dict())
            res.status_code = 201
            return group.to_dict()
    except (BaseORMException, RedisError):
        raise x.BadError()
    
@grouprouter.patch('', summary='Rename a Group')
async def update_group(res: Response, groupdata: UpdateGroupPyd, user=Depends(current_user)):
    if not await user.has_perm('group.update'):
        raise x.PermissionDenied()
    try:
        group = await Group.get_or_none(pk=groupdata.id).only('id', 'name', 'summary')
        if not group:
            raise x.NotFoundError('Group')
        await group.update_group(groupdata)
        res.status_code = 204

        # Update the cache if exists
        oldkey = s.CACHE_GROUPNAME.format(group.name)
        newkey = s.CACHE_GROUPNAME.format(groupdata.name)
        if red.exists(oldkey):
            formatted_oldkey = red.formatkey(oldkey)
            formatted_newkey = red.formatkey(newkey)
            red.rename(formatted_oldkey, formatted_newkey)
    except (BaseORMException, RedisError):
        raise x.BADERROR_503()

@grouprouter.delete('', summary='Delete a Group', status_code=422)
async def delete_group(res: Response, user=Depends(current_user), group: str = Body(...)):
    if not await user.has_perm('group.delete'):
        raise x.PermissionDenied()
    if not group:
        raise x.FalsyDataError()
    
    try:
        if await Group.delete_group(group):
            res.status_code = 204
    except (BaseORMException, RedisError):
        raise x.BadError()
    
    # usermod = await UserMod.get_or_none(email=user.email).only('id')
    # if not usermod:
    #     raise x.NotFoundError('User')
    
    # group = await Group.get_or_none(name=group.strip()).only('id', 'name')
    # if not group:
    #     raise x.NotFoundError('Group')
    
    # partialkey = s.CACHE_GROUPNAME.format(group.name)
    # await group.delete()
    # red.delete(partialkey)
    # res.status_code = 204
    