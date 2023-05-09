from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from ...core.db import get_session
from ...core.user import current_superuser
from ..jobs import delete_old_articles_job, start_parsers_job

SPIDERS = ['rbc_spider', 'inosmi_spider']

router = APIRouter()


@router.post('/', dependencies=[Depends(current_superuser)])
async def start_parsers(
    session: AsyncSession = Depends(get_session)
):
    """Эндпоинт для ручного запуска парсеров."""
    return await start_parsers_job(session)


@router.delete('/', dependencies=[Depends(current_superuser)])
async def delete_old_articles(
    session: AsyncSession = Depends(get_session),
    days: int = settings.STORAGE_DAYS
):
    """Эндпоинт для ручного запуска очистки БД."""
    return await delete_old_articles_job(session)
