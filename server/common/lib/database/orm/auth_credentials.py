from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, Boolean, DateTime, Integer, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from lib import TimeZone
from lib.database import DB


class AuthCredentials(DB.Base):
    __tablename__ = 'auth_credentials'

    id = Column(Text(), nullable=False, primary_key=True, unique=True, default=lambda: str(uuid4()))
    username = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False,)
    token = Column(Text(), nullable=True, unique=True, default=None)
    token_due = Column(DateTime(timezone=True), nullable=True, default=None)
    enable = Column(Boolean(), nullable=False, default=True)
    created_by = Column(Text(), nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(TimeZone.JST))
    updated_by = Column(Text(), nullable=True, default=None)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(TimeZone.JST))
    version = Column(Integer(), nullable=False, default=1)

    @classmethod
    async def by_id(cls, id: str, session: AsyncSession) -> Union['AuthCredentials', None]:
        query = select(cls).where(cls.id == id)
        records = await session.execute(query)
        record = records.scalars().first()
        return record

    @classmethod
    async def by_username(cls, username: str, session: AsyncSession) -> Union['AuthCredentials', None]:
        query = select(cls).where(cls.username == username)
        records = await session.execute(query)
        record = records.scalars().first()
        return record

    @classmethod
    async def by_token(cls, token: str, session: AsyncSession) -> Union['AuthCredentials', None]:
        query = select(cls).where(cls.token == token)
        records = await session.execute(query)
        record = records.scalars().first()
        return record


__all__ = [
    'AuthCredentials',
]
