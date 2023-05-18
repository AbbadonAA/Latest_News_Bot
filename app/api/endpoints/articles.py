from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from ...core.db import get_session
from ...core.user import current_superuser, current_user
from ...crud.articles import (get_article_amount_from_db,
                              get_article_by_id_from_db, get_articles_from_db,
                              mark_articles_as_read)
from ...filters.articles import CategoryFilter, SourceFilter
from ...models import UserModel
from ...schemas.articles import Article

router = APIRouter()
templates = Jinja2Templates('app/api/templates')


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
    source: SourceFilter = None,
    category_filter: CategoryFilter = None,
):
    """Получение статей с ограничением количества и фильтром категорий."""
    articles = (
        await get_articles_from_db(
            user,
            session,
            category_filter.value if category_filter else None,
            source.value if source else None,
        )
    )
    if articles:
        await mark_articles_as_read(user, articles, session)
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


@router.get('/html/{article_id}', response_class=HTMLResponse)
async def get_article_html(
    article_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Получение статьи в формате html."""
    article = await get_article_by_id_from_db(session, article_id)
    if not article:
        data = {'days': settings.STORAGE_DAYS}
        return templates.TemplateResponse(
            '404.html',
            {'request': request, **data},
            status_code=HTTPStatus.NOT_FOUND,
        )
    infographic_links = [
        link.infographic_link for link in article.infographic_links
    ]
    authors = [author.author_name for author in article.authors]
    data = {
        'title': article.title,
        'date': article.date,
        'category': article.category,
        'overview': article.overview,
        'original_link': article.link,
        'text': article.text.split('\n'),
        'picture': article.picture_link,
        'infographics': infographic_links,
        'video': article.video_link,
        'authors': authors,
        'source': article.source
    }
    return templates.TemplateResponse(
        'article.html',
        {'request': request, **data},
        status_code=HTTPStatus.OK,
    )
