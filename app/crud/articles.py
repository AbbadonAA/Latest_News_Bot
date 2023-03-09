from app.core.db import get_async_session
from app.models.articles import Article, Author, Infographic
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from scrapy import Item


async def add_articles(session: AsyncSession, item: Item) -> None:
    """Добавление статей в БД."""
    # Возвращаем количество добавленных статей.
    # Здесь запуск парсеров.
    # До запуска - замер количества статей. После - ещё замер.
    # Возвращаем схему с разницей = количество добавленных.
    ...


async def get_article_amount(session: AsyncSession) -> None:
    """Подсчет количества статей в БД."""
    # Добавить в схемы - схема ответа с количеством статей в БД.
    ...


async def check_article_existence(
    session: AsyncSession, link: str
 ) -> Optional[bool]:
    """Проверка наличия статьи в БД по ссылке."""
    # Возвращает True / False
    ...


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
