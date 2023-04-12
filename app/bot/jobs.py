from app.core.db import get_session
from app.crud.articles import get_articles_from_db
from app.crud.user import (create_user, get_user_article_limit_from_db,
                           get_user_by_chat_id_from_db,
                           update_user_article_limit_db)


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


async def get_user_article_limit(chat_id: int):
    """Получение article_limit пользователя."""
    sessions = get_session()
    async for session in sessions:
        article_limit = await get_user_article_limit_from_db(session, chat_id)
    return article_limit


async def update_user_article_limit(chat_id: int, article_limit: int):
    """Изменение article_limit пользователя."""
    sessions = get_session()
    async for session in sessions:
        article_limit = (
            await update_user_article_limit_db(
                session,
                chat_id,
                article_limit
            )
        )
    return article_limit


async def get_articles(chat_id: int, category: str, source: str):
    """Получение статей."""
    user = await get_or_create_user(chat_id)
    sessions = get_session()
    async for session in sessions:
        articles = await get_articles_from_db(user, session, category, source)
    return articles
