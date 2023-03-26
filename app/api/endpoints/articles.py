from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_session
from ...core.user import current_superuser, current_user
from ...crud.articles import (get_article_amount_from_db,
                              get_article_by_id_from_db, get_articles_from_db)
from ...filters.articles import SourceFilter, ThemeFilter
from ...models import UserModel
from ...schemas.articles import Article

router = APIRouter()


@router.get('/count', dependencies=[Depends(current_superuser)])
async def get_article_amount(session: AsyncSession = Depends(get_session)):
    """Получение количества статей в БД."""
    article_amount = await get_article_amount_from_db(session)
    ans = {'article_amount': article_amount}
    return ans


@router.get('/', response_model=list[Article])
async def get_articles(
    user: UserModel = Depends(current_user),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=10, gt=0, le=10),
    source: SourceFilter = None,
    category_filter: ThemeFilter = None,
):
    """Получение статей с ограничением количества и фильтром категорий."""
    articles = (
        await get_articles_from_db(
            user,
            session,
            limit,
            category_filter.value if category_filter else None,
            source.value if source else None,
        )
    )
    return articles


@router.get(
    '/{article_id}',
    response_model=Article,
    dependencies=[Depends(current_superuser)]
)
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
