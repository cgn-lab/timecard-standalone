from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Boolean, DateTime, Integer, Text
from lib import TimeZone
from lib.database import DB


class AuthCredentials(DB.Base):
    __tablename__ = 'auth_credentials'

    id = Column(Text(), nullable=False, primary_key=True, unique=True, default=lambda: str(uuid4()))
    username = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False,)
    token = Column(Text(), nullable=True, unique=True)
    token_due = Column(DateTime(timezone=True), nullable=True)
    refresh_token = Column(Text(), nullable=True, unique=True)
    refresh_token_due = Column(DateTime(timezone=True), nullable=True)
    salt = Column(Text(), nullable=True,)
    enable = Column(Boolean(), nullable=False, default=True)
    created_by = Column(Text(), nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(TimeZone.JST))
    updated_by = Column(Text(), nullable=True, default=None)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(TimeZone.JST))
    version = Column(Integer(), nullable=False, default=1)


__all__ = [
    'AuthCredentials',
]
