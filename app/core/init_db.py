# Создание первого суперпользователя при подключении к БД.
from app.core.config import settings
from app.crud.user import create_user


async def create_first_superuser():
    if (settings.first_superuser_email is not None
        and settings.first_superuser_password is not None
            and settings.first_superuser_chat_id is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            chat_id=settings.first_superuser_chat_id,
            is_superuser=True,
        )
