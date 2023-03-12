from typing import Optional

from scrapy import Item
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.articles import Article, Author, Infographic


async def add_article(session: AsyncSession, item: Item) -> Article:
    """Добавление статьи в БД."""
    article = Article(
        date=item['date'],
        category=item['category'],
        title=item['title'],
        overview=item['overview'],
        text=item['text'],
        link=item['link'],
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
            await add_article_author(session, article_id, author)
    if infographic_links:
        for infographic_link in infographic_links:
            await add_article_infographics(
                session, article_id, infographic_link
            )
    return article


async def add_article_author(
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


async def add_article_infographics(
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


async def get_article_amount(session: AsyncSession) -> int:
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


async def get_article_by_id(
    session: AsyncSession,
    id: int
) -> None:
    """Получение статьи по её id в БД."""
    # Возвращается схема статьи, полученной из БД.
    ...


async def get_filtered_articles(
    session: AsyncSession,
    amount: int,
    filter: Optional[str]
) -> None:
    """Получение amount статей, отфильтрованных по теме filter."""
    # Вернуть список статей - list[схема для статьи]
    ...
