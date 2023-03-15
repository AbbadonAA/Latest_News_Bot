from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_session
from ...crud.articles import get_article_amount_from_db, get_articles_from_db
from ...schemas.articles import Article

router = APIRouter()


@router.get('/', response_model=list[Article])
async def get_all_articles(
    session: AsyncSession = Depends(get_session),
    limit: str | None = None,
    filter: str | None = None
):
    """Получение статей с ограничением количества и фильтром категорий."""
    articles = await get_articles_from_db(session, limit, filter)
    return articles


@router.get('/count')
async def get_article_amount(session: AsyncSession = Depends(get_session)):
    """Получение выбранного количества новых статей."""
    article_amount = await get_article_amount_from_db(session)
    ans = {
        'article_count': article_amount,
    }
    return ans
