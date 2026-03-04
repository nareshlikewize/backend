
from fastapi import APIRouter
from ...repositories import postgres

router = APIRouter(prefix='/users', tags=['users'])

@router.get('')
def list_users():
    return postgres.list_users()

@router.post('')
def create_user(user: dict):
    return postgres.create_user(email=user['email'], name=user.get('name',''))

@router.get('/roles')
def list_roles():
    return postgres.list_roles()
