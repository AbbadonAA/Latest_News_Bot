import aiofiles
from loguru import logger
from telegram import InputFile
from telegram.ext import ContextTypes

from app.core.config import BASE_DIR, settings
from app.core.db import get_session
from app.crud.articles import get_articles_from_db, mark_articles_as_read
from app.crud.user import (create_user, get_user_article_limit_from_db,
                           get_user_by_chat_id_from_db,
                           update_user_article_limit_db)
from app.filters.articles import CategoryFilter, SourceFilter
from app.models.articles import Article

from .menu import article_keyboard, get_article_url

IMG_NOT_FOUND_PATH = str(
    BASE_DIR / "app" / "api" / "templates" / 'img_not_found.png')


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
        if articles:
            await mark_articles_as_read(user, articles, session)
    return articles


async def get_picture_for_msg(article: Article) -> str:
    """Получение картинки для превью статьи."""
    picture = article.picture_link
    if not picture:
        logger.info(f'Статья {article.id}: нет изображения для превью.')
        infographics = [
            link.infographic_link for link in article.infographic_links
        ]
        video_preview = article.video_preview_link
        if infographics:
            logger.info(f'Статья {article.id}: использована инфографика.')
            picture = infographics[0]
        elif video_preview:
            logger.info(f'Статья {article.id}: использовано превью из видео.')
            picture = video_preview
        else:
            logger.info(f'Статья {article.id}: использовано IMG_NOT_FOUND.')
            async with aiofiles.open(IMG_NOT_FOUND_PATH, 'rb') as f:
                content = await f.read()
            picture = InputFile(content)
    return picture


async def send_article_message(
    article: Article,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    """Отправка сообщения со статьей пользователю"""
    title = article.title
    category = article.category
    overview = article.overview
    if not overview:
        overview = ''
    else:
        overview += '\n\n'
    msg_text = (
        f'<b>{title}</b>\n\n'
        f'{overview}'
        f'<i>Категория: {category}</i>\n'
        f'<i>Источник: {article.source}</i>'
    )
    picture = await get_picture_for_msg(article)
    keyboard = article_keyboard(article.id)
    await context.bot.send_photo(
        chat_id,
        photo=picture,
        caption=msg_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def send_article_iv_template(
    article: Article,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Отправка ссылки на шаблон Instant View."""
    url = get_article_url(article.id)
    url = f'https://t.me/iv?url={url}&rhash={settings.RHASH}'
    await context.bot.send_message(chat_id, url)


async def send_article(
    article: Article,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    iv: bool = settings.INSTANT_VIEW
):
    """Отправка статьи пользователю."""
    if iv and settings.RHASH:
        await send_article_iv_template(article, chat_id, context)
    else:
        await send_article_message(article, chat_id, context)


async def send_article_set_description(
    chat_id: int,
    source: str,
    category: str,
    context: ContextTypes.DEFAULT_TYPE
):
    msg_txt = f'Статьи из {source}'
    if source == SourceFilter.ALL:
        msg_txt = 'Статьи из всех источников'
    if category == CategoryFilter.ALL:
        msg_txt += ' по всем темам:'
    else:
        msg_txt += f' на тему {category}:'
    await context.bot.send_message(chat_id, msg_txt)


async def send_not_found_msg(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.info(f'Пользователь {chat_id} не получил статьи по запросу.')
    msg_text = (
        'К сожалению новых статей по выбранным параметрам не найдено. '
        'Попробуйте позже или измените параметры.'
    )
    await context.bot.send_message(chat_id, text=msg_text)
