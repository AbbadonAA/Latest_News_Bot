import contextlib

from fastapi_users.exceptions import UserAlreadyExists
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
        chat_id: int,
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
    return user.scalar()
