import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from ...core.db import get_session
from ...core.user import current_superuser
from ...crud.articles import (delete_old_articles_from_db,
                              get_article_amount_from_db)

SPIDERS = ['rbc_spider', 'inosmi_spider']

router = APIRouter()


async def async_run(args, cwd=None):
    """Асинхронный запуск подпроцессов, чтобы не блокировать приложение."""
    process = await asyncio.create_subprocess_exec(*args, cwd=cwd)
    await process.communicate()


@router.post('/', dependencies=[Depends(current_superuser)])
async def start_parsers(
    session: AsyncSession = Depends(get_session)
):
    """Запуск парсеров для заполнения БД."""
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
    return {'result': f'В БД успешно добавлено {num_added} записей.'}


@router.delete('/', dependencies=[Depends(current_superuser)])
async def delete_old_articles(
    session: AsyncSession = Depends(get_session),
    days: int = settings.DAYS
):
    """Удаление статей, дата кот. отстает от текущей больше, чем на days."""
    count_before_del = await get_article_amount_from_db(session)
    await delete_old_articles_from_db(session, days)
    count_after_del = await get_article_amount_from_db(session)
    num_deleted = count_before_del - count_after_del
    return {'result': f'Из БД успешно удалено {num_deleted} старых статей.'}
