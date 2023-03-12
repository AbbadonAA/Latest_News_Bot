from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...crud.articles import get_article_amount
from ...core.db import get_session

router = APIRouter()


@router.get('/get_news')
async def get_articles(session: AsyncSession = Depends(get_session)):
    """Получение выбранного количества новых статей."""
    article_amount = await get_article_amount(session)
    ans = {
        'article_count': article_amount,
    }
    return ans
