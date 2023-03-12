# from app.core.db import get_async_session
# from app.core.config import settings
from app.core.db import engine
from app.crud.articles import add_article
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# engine = create_async_engine(settings.db_scrapy_url)


class ArticlesToDBPipeline:
    """Запись полученных пауком статей (item) в БД."""

    def open_spider(self, spider):
        self.AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
        # db_gen = get_async_session()
        # self.session = db_gen.asend(None)

    async def process_item(self, item, spider):
        # тут добавить проверку наличия статьи
        # добавляется статья, если такой ещё нет в БД

        async with self.AsyncSessionLocal() as session:
            await add_article(session, item)
            return item
