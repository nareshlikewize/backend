
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, MetaData, UniqueConstraint

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(255), unique=True, nullable=False),
    Column('name', String(255), nullable=False),
    Column('is_active', Boolean, default=True)
)

roles = Table(
    'roles', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), unique=True, nullable=False)
)

user_roles = Table(
    'user_roles', metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    UniqueConstraint('user_id', 'role_id', name='uq_user_role')
)
