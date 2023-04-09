from datetime import datetime, timedelta
from typing import Optional

from dateutil.tz import tzlocal
from scrapy import Item
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Article, ArticleUser, Author, Infographic, UserModel


async def add_article_to_db(session: AsyncSession, item: Item) -> Article:
    """Добавление статьи в БД."""
    article = Article(
        date=item['date'],
        category=item['category'],
        title=item['title'],
        overview=item['overview'],
        text=item['text'],
        link=item['link'],
        video_link=item['video_link'],
        picture_link=item['picture_link'],
        source=item['source']
    )
    session.add(article)
    await session.commit()
    await session.refresh(article)
    article_id = article.id
    authors = item['authors']
    infographic_links = item['infographic_links']
    if authors:
        for author in authors:
            await add_article_author_to_db(session, article_id, author)
    if infographic_links:
        for infographic_link in infographic_links:
            await add_article_infographics_to_db(
                session, article_id, infographic_link
            )
    return article


async def add_article_author_to_db(
    session: AsyncSession, article_id: int, author_name: str
) -> Author:
    """Добавление авторов статьи в БД."""
    article_author = Author(
        article_id=article_id,
        author_name=author_name
    )
    session.add(article_author)
    await session.commit()
    await session.refresh(article_author)
    return article_author


async def add_article_infographics_to_db(
    session: AsyncSession, article_id: int, infographic_link: str
) -> Infographic:
    """Добавление инфографики статьи в БД."""
    infographic = Infographic(
        article_id=article_id,
        infographic_link=infographic_link
    )
    session.add(infographic)
    await session.commit()
    await session.refresh(infographic)
    return infographic


async def get_article_amount_from_db(session: AsyncSession) -> int:
    """Подсчет количества статей в БД."""
    amount = await session.scalar(select(func.count()).select_from(Article))
    return amount


async def check_article_existence(
    session: AsyncSession, link: str
 ) -> Optional[bool]:
    """Проверка наличия статьи в БД по ссылке."""
    existence = await session.execute(
        select(
            select(Article)
            .where(Article.link == link)
            .exists()
        )
    )
    return existence.scalar()


async def mark_articles_as_read(
    user: UserModel, articles: list[Article], session: AsyncSession
):
    """Помечание статей прочитанных пользователем."""
    article_users = [
        ArticleUser(
            article_id=article.id, user_id=user.id) for article in articles
    ]
    session.add_all(article_users)
    await session.commit()


async def get_articles_from_db(
    user: UserModel,
    session: AsyncSession,
    category_filter: str,
    source: str
) -> list[Article]:
    """Получение списка статей."""
    stmt = select(Article).options(selectinload(Article.readers))
    if source and source != 'ВСЕ':
        stmt = stmt.where(Article.source == source)
    if category_filter and category_filter != 'ВСЕ':
        stmt = stmt.where(Article.category == category_filter)
    # Исключение статей, которые пользователь уже читал.
    stmt = stmt.filter(~Article.readers.contains(user))
    articles = await session.execute(
        stmt
        .order_by(Article.date.desc())
        .limit(user.article_limit)
    )
    articles = articles.scalars().all()
    if articles:
        await mark_articles_as_read(user, articles, session)
    return articles


async def get_article_by_id_from_db(
    session: AsyncSession,
    article_id: int
) -> Article:
    """Получение статьи по её id в БД."""
    stmt = select(Article).where(Article.id == article_id)
    article = await session.execute(stmt)
    return article.scalar()


async def delete_old_articles_from_db(
    session: AsyncSession,
    days: int,
) -> None:
    """Удаление устаревших статей."""
    now_datetime = datetime.now(tzlocal()).replace(microsecond=0)
    min_datetime = (now_datetime - timedelta(days=days))
    stmt = delete(Article).where(Article.date < min_datetime)
    await session.execute(stmt)
    await session.commit()
