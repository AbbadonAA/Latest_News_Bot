import scrapy
from ..items import ArticleItem
# from ..settings import STANDART_CATEGORIES


INOSMI_CATEGORIES = {'Политика', 'Экономика', 'Общество'}


class InosmiSpider(scrapy.Spider):
    name = "inosmi_spider"
    allowed_domains = ["inosmi.ru"]
    start_urls = ["https://inosmi.ru"]

    def parse(self, response):
        """Парсинг заголовка главной страницы и переход в категории."""
        header_buttons = (response.css('div.cell-extension__list')
                          .css('div.cell-extension__item-bg'))
        for button in header_buttons:
            category = button.css('span::text').get()
            link = self.start_urls[0] + button.css('a::attr(href)').get()
            if category in INOSMI_CATEGORIES:
                yield response.follow(
                    link,
                    callback=self.parse_category,
                    meta={'category': category}
                )

    def parse_category(self, response):
        """Парсинг ссылок на статьи на странице категории."""
        # в рамках проекта достаточно ссылок на первой стр. (без прокрутки).
        articles = response.css('div.list-item')
        # отсюда: заголовок (источник + заголовок), картинка, ссылка на статью
        # переход в статью для парсинга текста.
        for article in articles:
            article_link = article.css('div.list-item__source').css('a.list-item__title::text').get()
            yield {'article_link': article_link}

    # def parse_article(self, response):
    #     ...
