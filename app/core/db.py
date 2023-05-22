from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import settings


class PreBase():

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(
    settings.database_url, future=True, echo=False, pool_size=50)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session_maker() as session:
        yield session
