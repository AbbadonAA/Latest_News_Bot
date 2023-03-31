from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

from ...core.db import get_session
from ...core.user import current_superuser
from ...crud.user import get_all_users_from_db

router = APIRouter()


@router.get(
    '/users/all',
    tags=['Пользователи'],
    dependencies=[Depends(current_superuser)],
    response_model=list[UserRead]
)
async def get_all_users(
    session: AsyncSession = Depends(get_session)
):
    """Получение списка всех пользователей приложения."""
    users = await get_all_users_from_db(session)
    return users

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Регистрация и авторизация']
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Регистрация и авторизация']
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['Пользователи']
)
