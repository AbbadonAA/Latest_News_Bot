from telegram.ext import ContextTypes

from app.core.db import get_session
from app.crud.articles import get_articles_from_db
from app.crud.user import (create_user, get_user_article_limit_from_db,
                           get_user_by_chat_id_from_db,
                           update_user_article_limit_db)
from app.models.articles import Article

from .menu import article_keyboard


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


async def send_article(
    article: Article,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    """Отправка статьи пользователю"""
    title = article.title
    picture = article.picture_link
    if not picture:
        # Временная заглушка. Потом нужна своя картинка из templates.
        picture = 'https://t-bike.ru/images/products/no-image.jpg'
    overview = article.overview
    if not overview:
        overview = ''
    else:
        overview += '\n\n'
    category = article.category
    msg_text = (
        f'<b>{title}</b>\n\n'
        f'{overview}'
        f'<i>Категория: {category}</i>'
    )
    keyboard = article_keyboard(article.id)
    await context.bot.send_photo(
        chat_id,
        photo=picture,
        caption=msg_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def send_article_set_description(
    chat_id: int,
    source: str,
    category: str,
    context: ContextTypes.DEFAULT_TYPE
):
    msg_txt = f'Статьи из {source}'
    if source == 'ВСЕ':
        msg_txt = 'Статьи из всех источников'
    if category == 'ВСЕ':
        msg_txt += ' по всем темам:'
    else:
        msg_txt += f' на тему {category}:'
    await context.bot.send_message(chat_id, msg_txt)


async def send_not_found_msg(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    msg_text = (
        'К сожалению новых статей по выбранным параметрам не найдено. '
        'Попробуйте позже или измените параметры.'
    )
    await context.bot.send_message(chat_id, text=msg_text)