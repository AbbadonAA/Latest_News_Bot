import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from loguru import logger
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

from ..models import UserModel

get_async_session_context = contextlib.asynccontextmanager(get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr,
        password: str,
        chat_id: int = None,
        is_superuser: bool = False
):
    """Создание пользователя."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            chat_id=chat_id,
                            is_superuser=is_superuser
                        )
                    )
                    logger.info(f'Создан пользователь: {user.chat_id}.')
                    return user
    except UserAlreadyExists:
        pass


async def get_all_users_from_db(
    session: AsyncSession,
) -> list[UserModel]:
    """Получение списка пользователей."""
    stmt = select(UserModel)
    users = await session.execute(stmt)
    return users.scalars().all()


async def get_user_by_chat_id_from_db(
    session: AsyncSession,
    chat_id: int
) -> UserModel:
    """Получение пользователя по chat_id."""
    stmt = select(UserModel).where(UserModel.chat_id == chat_id)
    user = await session.execute(stmt)
    # Добавить raise Exception, если не найден.
    return user.scalar()


async def update_user_article_limit_db(
    session: AsyncSession,
    chat_id: int,
    article_limit: int
) -> int:
    """Изменение article_limit пользователя."""
    user = await get_user_by_chat_id_from_db(session, chat_id)
    user.article_limit = article_limit
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user.article_limit


async def get_user_article_limit_from_db(
    session: AsyncSession,
    chat_id: int
) -> int:
    """Получение актуального лимита статей пользователя."""
    stmt = select(UserModel.article_limit).where(UserModel.chat_id == chat_id)
    article_limit = await session.execute(stmt)
    return article_limit.scalar()
