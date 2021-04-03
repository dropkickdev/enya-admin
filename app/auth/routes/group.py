from fastapi import Request, Depends, Body, APIRouter

from app.auth import current_user
from . import UserGroupPy, CreateGroupPy, UpdateGroupPy


grouprouter = APIRouter()

# PLACEHOLDER: create_group()
@grouprouter.post('', summary='Create a new Group')
async def create_group(_: Request, name: CreateGroupPy, user=Depends(current_user)):
    return True

# PLACEHOLDER: update_group()
@grouprouter.patch('', summary='Rename a Group')
async def update_group(_: Request, rel: UpdateGroupPy, user=Depends(current_user)):
    pass

# PLACEHOLDER: delete_group()
@grouprouter.delete('', summary='Delete a Group')
async def delete_group(_: Request, user=Depends(current_user), id: int = Body(...)):
    pass

# PLACEHOLDER: assign_usergroup()
@grouprouter.post('/assign', summary='Assign a Group to a User')
async def assign_grouptouser(_: Request, rel: UserGroupPy, user=Depends(current_user)):
    pass

# PLACEHOLDER: remove_usergroup()
@grouprouter.delete('/remove', summary='Remove a Group from a User')
async def remove_groupfromuser(_: Request, rel: UserGroupPy, user=Depends(current_user)):
    pass