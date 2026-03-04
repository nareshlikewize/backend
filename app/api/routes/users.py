
from fastapi import APIRouter
from ...services.store import USERS, ROLES

router = APIRouter(prefix='/users', tags=['users'])

@router.get('')
def list_users():
    return USERS

@router.post('')
def create_user(user: dict):
    new_id = max([u['id'] for u in USERS] + [0]) + 1
    USERS.append({"id": new_id, "email": user['email'], "name": user.get('name',''), "is_active": True})
    return USERS[-1]

@router.get('/roles')
def list_roles():
    return ROLES
