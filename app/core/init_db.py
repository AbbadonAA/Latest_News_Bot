# Создание первого суперпользователя при подключении к БД.
from app.core.config import settings
from app.crud.user import create_user


async def create_first_superuser():
    if (settings.FIRST_SUPERUSER_EMAIL is not None
        and settings.FIRST_SUPERUSER_PASSWORD is not None
            and settings.FIRST_SUPERUSER_CHAT_ID is not None):
        await create_user(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            chat_id=settings.FIRST_SUPERUSER_CHAT_ID,
            is_superuser=True,
        )
