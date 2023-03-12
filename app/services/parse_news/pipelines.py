from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.db import engine
from app.crud.articles import add_article, check_article_existence


class ArticlesToDBPipeline:
    """Запись полученных пауком статей (item) в БД."""

    def open_spider(self, spider):
        self.AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

    async def process_item(self, item, spider):
        # тут добавить проверку наличия статьи
        # добавляется статья, если такой ещё нет в БД

        async with self.AsyncSessionLocal() as session:
            item_in_db = await check_article_existence(session, item['link'])
            if not item_in_db:
                await add_article(session, item)
            return item
