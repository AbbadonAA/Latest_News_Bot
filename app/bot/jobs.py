from app.core.db import get_session
from app.crud.user import create_user, get_user_by_chat_id_from_db


async def get_or_create_user(chat_id: int):
    """Получение или создание пользователя."""
    email = str(chat_id) + '@app.ru'
    password = str(chat_id)
    sessions = get_session()
    async for session in sessions:
        user = await get_user_by_chat_id_from_db(session, chat_id)
        if not user:
            user = await create_user(email, password, chat_id, False)
    return user
