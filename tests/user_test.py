import pytest, json
from pydantic import UUID4

from app import ic
from app.auth import current_user, user_data
from app.cache import red
from .auth_test import VERIFIED_USER_DEMO, VERIFIED_EMAIL_DEMO, ACCESS_TOKEN_DEMO


# @pytest.mark.userdata
# # @pytest.mark.skip
# def test_current_user_data(client, passwd, headers):
#     res = client.post('/test/dev_user_data', headers=headers)
#     data = res.json()
#     # ic(data)
#     assert data.get('id') == VERIFIED_USER_DEMO
#     assert data.get('email') == VERIFIED_EMAIL_DEMO
#     assert type(data.get('is_active')) == bool
#     assert type(data.get('groups')) == list


# @pytest.mark.focus
def test_user_data(loop):
    async def ab():
        return await user_data(VERIFIED_USER_DEMO)

    user = loop.run_until_complete(ab())
    assert isinstance(user.id, UUID4)
    assert isinstance(user.groups, list)
    assert isinstance(user.is_active, bool)
    assert isinstance(user.options, dict)
    assert isinstance(user.email, str)

    with pytest.raises(AttributeError):
        hasattr(user.permissions, 'permissions')


# param = [
#     ('StaffGroup', {'ContentGroup', 'AccountGroup', 'StaffGroup'}),
#     (['AdminGroup', 'ContributorGroup'], {'ContentGroup', 'AccountGroup', 'StaffGroup', 'AdminGroup', 'ContributorGroup'}),
#     ('rollback', True)
# ]
# @pytest.mark.parametrize('add, out', param)
# # @pytest.mark.focus
# # @pytest.mark.skip
# def test_user_add_group(client, headers, add, out):
#     data = json.dumps(add)
#     res = client.post('/test/dev_user_add_group', headers=headers, data=data)
#     data = res.json()
#
#     if add == 'rollback':
#         assert data
#     else:
#         assert set(data.get('groups')) == out
#
#
# param = [
#     ('ContentGroup', True), (['ContentGroup'], True), (['ContentGroup', 'AccountGroup'], True),
#     ([], False), ('', False),
#     (['ContentGroup', 'AccountGroup', 'x'], False),
# ]
# @pytest.mark.parametrize('groups, out', param)
# # @pytest.mark.focus
# def test_user_has_group(client, groups, out, headers):
#     data = json.dumps(dict(groups=groups))
#     res = client.post('/test/dev_user_has_group', headers=headers, data=data)
#     data = res.json()
#     assert data == out
#
#
# param = [
#     ('settings.read', True),
#     (['settings.read'], True),
#     ('foo.read', False), (['foo.read'], False), (['foo.read', 'foo.update'], False),
#     (['settings.read', 'page.read'], True),
#     (('settings.read', 'page.read'), True),
#     (['settings.read', 'page.read', 'foo.read'], False),
#     ('', False), ([], False)
# ]
# @pytest.mark.parametrize('perms, out', param)
# # @pytest.mark.focus
# # @pytest.mark.skip
# def test_has_perm(client, headers, perms, out):
#     data = json.dumps(perms)
#     res = client.post('/test/dev_user_has_perms', headers=headers, data=data)
#     data = res.json()
#     assert data == out
#
#
# param = [
#     ('Temp1', True), (['Temp1'], True), (['Temp1', 'Temp2'], True),
#     ('', False), ([], False), (None, False), (True, False), (False, False),
# ]
# @pytest.mark.parametrize('data, out', param)
# # @pytest.mark.focus
# @pytest.mark.skip
# def test_remove_user_permissions(client, headers, data, out):
#     data = json.dumps(data)
#     res = client.post('/test/dev_remove_user_permissions', headers=headers, data=data)
#     data = res.json()
#     # assert data == out













# # @pytest.mark.focus
# @pytest.mark.skip
# def test_add_perm(client, headers):
#     res = client.post('/test/dev_user_add_perm', headers=headers)
#     data = res.json()
#     # ic(data)
#     assert data.get('id') == VERIFIED_USER_ID
#     assert data.get('email') == VERIFIED_EMAIL_DEMO
#     assert data.get('groups'), 'User needs to have at least one (1) group'
#     # assert data.get('permissions'), 'User needs to have at least one (1) permission'
#     # assert data.get('options'), 'User needs to have at least one (1) option'
