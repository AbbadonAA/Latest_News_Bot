from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from ...core.db import get_session
from ...crud.articles import delete_old_articles_from_db

router = APIRouter()


@router.post('/')
async def start_parsers():
    """Запуск парсеров для заполнения БД."""
    return {'result': 'Парсинг завершен. В БД добавлено N записей.'}


@router.delete('/')
async def delete_old_articles(
    session: AsyncSession = Depends(get_session),
    days: int = settings.DAYS
):
    """Удаление статей, дата кот. отстает от текущей больше, чем на days."""
    await delete_old_articles_from_db(session, days)
    return {'result': 'Устаревшие данные удалены из БД'}
