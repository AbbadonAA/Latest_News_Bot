from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_session
from ...crud.articles import (get_article_amount_from_db,
                              get_article_by_id_from_db, get_articles_from_db)
from ...filters.articles import ThemeFilter
from ...schemas.articles import Article

router = APIRouter()


@router.get('/count')
async def get_article_amount(session: AsyncSession = Depends(get_session)):
    """Получение количества статей в БД."""
    article_amount = await get_article_amount_from_db(session)
    ans = {'article_amount': article_amount}
    return ans


@router.get('/', response_model=list[Article])
async def get_articles(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=10, gt=0, le=10),
    filter: ThemeFilter = None
):
    """Получение статей с ограничением количества и фильтром категорий."""
    articles = (
        await get_articles_from_db(
            session, limit, filter.value if filter else None)
    )
    return articles


@router.get('/{article_id}', response_model=Article)
async def get_article_by_id(
    article_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Получение статьи по id."""
    article = await get_article_by_id_from_db(session, article_id)
    if not article:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такой статьи нет в БД.')
    return article
