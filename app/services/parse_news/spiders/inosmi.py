import datetime as dt

import scrapy

from ..items import ArticleItem

INOSMI_CATEGORIES = {'Политика', 'Экономика', 'Общество'}
SOURCE = 'ИноСМИ'


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
        articles = response.css('div.list-item__content')
        for article in articles:
            source = article.css('div.source').css('a::text').get()
            title = article.css('a.list-item__title::text').get()
            if title:
                title = title.strip()
            if source:
                title = source + ': ' + title
            category = response.meta.get('category')
            link = article.css('a.list-item__title::attr(href)').get()
            link = self.start_urls[0] + link
            yield response.follow(
                link,
                callback=self.parse_article,
                meta={'category': category, 'title': title}
            )

    def parse_article(self, response):
        """Парсинг данных в статье."""
        date = response.css('div.endless__item::attr(data-published)').get()
        date = dt.datetime.fromisoformat(date)
        overview = response.css('div.article__announce-text::text').get()
        if overview:
            overview = overview.strip()
        text = response.css('div.article__text')
        text = [txt.xpath('string()').get().strip() for txt in text]
        if text:
            exclude = 'Читайте ИноСМИ в'
            text = '\n'.join(t.strip() for t in text if exclude not in t)
        authors = (response
                   .css('div.article__authors-item')
                   .css('a::text').getall())
        picture_link = response.css('div.media').css('img::attr(src)').get()
        video_link = response.css('div.media').css('iframe::attr(src)').get()
        video_preview_link = response.css(
            'div[itemprop="image"] a[itemprop="url"]::attr(href)').get()
        infographic_links = []
        article = dict(
            date=date,
            category=response.meta.get('category'),
            title=response.meta.get('title'),
            overview=overview,
            text=text,
            link=response.request.url,
            picture_link=picture_link,
            video_link=video_link,
            video_preview_link=video_preview_link,
            infographic_links=infographic_links,
            authors=authors,
            source=SOURCE
        )
        yield ArticleItem(article)
