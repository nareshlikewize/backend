
from sqlalchemy import create_engine, select, insert, delete
from sqlalchemy.engine import Engine
from ..config.settings import settings
from ..models.user_models import metadata, users, roles, user_roles

_engine: Engine = create_engine(settings.DATABASE_URL, echo=False, future=True)
metadata.create_all(_engine)

def create_user(email: str, name: str):
    with _engine.begin() as conn:
        res = conn.execute(insert(users).values(email=email, name=name).returning(users))
        return res.first()._mapping

def list_users():
    with _engine.begin() as conn:
        res = conn.execute(select(users))
        return [dict(r._mapping) for r in res]

def add_role(name: str):
    with _engine.begin() as conn:
        res = conn.execute(insert(roles).values(name=name).returning(roles))
        return res.first()._mapping

def assign_role(user_id: int, role_id: int):
    with _engine.begin() as conn:
        conn.execute(insert(user_roles).values(user_id=user_id, role_id=role_id))

def list_roles():
    with _engine.begin() as conn:
        res = conn.execute(select(roles))
        return [dict(r._mapping) for r in res]
