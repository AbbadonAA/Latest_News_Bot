import datetime as dt
import json
import time

import scrapy
from ..items import ArticleItem


STANDART_CATEGORIES = {
    'Спорт', 'Политика', 'Бизнес', 'Финансы',
    'Общество', 'Экономика', 'Крипто'
}
LIMIT = 10
URL = ('https://www.rbc.ru/v10/ajax/get-news-feed-short/project/rbcnews.'
       'uploaded/lastDate/{}/limit/{}?_=')
SOURCE = 'РБК'


class RbcSpider(scrapy.Spider):
    name = "rbc_spider"
    allowed_domains = ["rbc.ru"]
    today = dt.datetime.now()
    from_time = int(time.mktime(today.timetuple()))
    yesterday = today - dt.timedelta(days=1)
    to_time = int(time.mktime(yesterday.timetuple()))
    start_urls = [URL.format(from_time, LIMIT)]

    def parse(self, response):
        """Парсинг бесконечной ленты новостей: сутки от текущего момента."""
        data = json.loads(response.text)
        last_time = 0
        for item in data.get('items'):
            selector = scrapy.Selector(text=item['html'], type='html')
            last_time = int(selector
                            .css('div.js-news-feed-item')
                            .xpath('@data-modif').get())
            category = selector.css('a.item__category::text').get()
            # Пропуск платных статей (отмечены img вместо текста в категории)
            if not category:
                continue
            category = category.replace(',', '').strip()
            title = selector.css('span.item__title::text').get().strip()
            # Пропуск нестандартных статей (онлайн репортажи и статьи РБК)
            if category not in STANDART_CATEGORIES or 'Онлайн' in title:
                continue
            link = selector.css('a.item__link::attr(href)').get().strip()
            yield response.follow(
                link,
                callback=self.parse_article,
                meta={'title': title, 'category': category})
        if last_time > self.to_time:
            yield response.follow(
                URL.format(last_time, LIMIT), callback=self.parse)

    def parse_article(self, response):
        """
        Парсинг отдельной статьи:
            дата, обзор, текст, изображение,
            инфографика, авторы
        """
        date = response.css('time.article__header__date::attr(datetime)').get()
        date = dt.datetime.fromisoformat(date)
        overview = (response.css('div.article__text__overview')
                    .css('span::text').get())
        if overview:
            overview = overview.strip()
        text = response.css('div.article__text').xpath('//p//text()').getall()
        if text:
            text = ' '.join(t.strip() for t in text)
        picture_link = (response.css('div.article__main-image__wrap')
                        .css('img::attr(src)').get())
        infographic_links = (response.css('div.g-mobile-visible')
                             .css('div.article__picture__wrap')
                             .css('img::attr(src)').getall())
        authors = (response.css('span.article__authors__author__name::text')
                   .getall())
        article = dict(
            date=date,
            category=response.meta.get('category'),
            title=response.meta.get('title'),
            overview=overview,
            text=text,
            link=response.request.url,
            picture_link=picture_link,
            infographic_links=infographic_links,
            authors=authors,
            source=SOURCE
        )
        yield ArticleItem(article)
