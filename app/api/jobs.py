import asyncio

import aioschedule as schedule
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_session

from ..crud.articles import (delete_old_articles_from_db,
                             get_article_amount_from_db)

SPIDERS = ['rbc_spider', 'inosmi_spider']


async def async_run(args, cwd=None):
    """Асинхронный запуск подпроцессов, чтобы не блокировать приложение."""
    process = await asyncio.create_subprocess_exec(*args, cwd=cwd)
    await process.communicate()


async def start_parsers_job(
    session: AsyncSession
):
    """Запуск парсеров для заполнения БД."""
    logger.info('Запущены парсеры для сбора новостных статей.')
    count_before_add = await get_article_amount_from_db(session)
    tasks = []
    # Пауки запускаются в отдельных асинхронных подпроцессах.
    for spider in SPIDERS:
        args = ["python", "-m", "scrapy.cmdline", "crawl", spider]
        task = asyncio.ensure_future(
            async_run(args, cwd='app/services/parse_news')
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
    count_after_add = await get_article_amount_from_db(session)
    num_added = count_after_add - count_before_add
    logger.info(
        f'Парсеры завершили работу. В БД добавлено {num_added} записей.'
    )
    return {'result': f'В БД успешно добавлено {num_added} записей.'}


async def delete_old_articles_job(
    session: AsyncSession,
    days: int = settings.STORAGE_DAYS
):
    """Удаление статей, дата кот. отстает от текущей больше, чем на days."""
    logger.info('Запущена очистка БД от старых записей.')
    count_before_del = await get_article_amount_from_db(session)
    await delete_old_articles_from_db(session, days)
    count_after_del = await get_article_amount_from_db(session)
    num_deleted = count_before_del - count_after_del
    logger.info(f'БД очищена - удалено {num_deleted} записей.')
    return {'result': f'Из БД успешно удалено {num_deleted} старых статей.'}


async def schedule_jobs():
    """Исполнение задач по расписанию."""
    sessions = get_session()
    async for session in sessions:
        schedule.every(
            settings.PARSER_FREQUENCY).minutes.do(start_parsers_job, session)
        schedule.every().day.at('00:00').do(delete_old_articles_job, session)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
