import datetime as dt
import time

import scrapy
import json


STANDART_CATEGORIES = {
    'Спорт', 'Политика', 'Бизнес', 'Финансы', 'Общество', 'Экономика'
}


class RbcSpider(scrapy.Spider):
    name = "rbc_spider"
    allowed_domains = ["rbc.ru"]
    source = 'rbc'
    today = dt.datetime.now()
    from_time = int(time.mktime(today.timetuple()))
    yesterday = today - dt.timedelta(days=1)
    to_time = int(time.mktime(yesterday.timetuple()))
    limit = 10
    url = ('https://www.rbc.ru/v10/ajax/get-news-feed-short/project/rbcnews.'
           'uploaded/lastDate/{}/limit/{}?_=')
    start_urls = [url.format(from_time, limit)]

    def parse(self, response):
        """Парсинг бесконечной ленты новостей: сутки от текущего момента."""
        data = json.loads(response.text)
        last_time = 0
        for item in data.get('items'):
            selector = scrapy.Selector(text=item['html'], type='html')
            last_time = int(selector.css(
                'div.js-news-feed-item').xpath('@data-modif').get())
            category = selector.css('a.item__category::text').get().replace(',', '').strip()
            title = selector.css('span.item__title::text').get().strip()
            # Пропуск платных статей (отмечены img вместо текста в категории)
            # Пропуск нестандартных статей (онлайн репортажи и статьи РБК)
            if category not in STANDART_CATEGORIES or 'Онлайн' in title:
                continue
            link = selector.css('a.item__link::attr(href)').get().strip()
            yield response.follow(link, callback=self.parse_article)
        if last_time > self.to_time:
            yield response.follow(
                self.url.format(last_time, self.limit), callback=self.parse)

    def parse_article(self, response):
        """
        Парсинг отдельной статьи:
            дата, категория, заголовок, обзор, текст,
            изображение, инфографика, авторы
        """
        date = response.css('time.article__header__date::attr(datetime)').get()
        category = response.css('a.article__header__category::text').get().strip()
        title = response.css('h1.article__header__title-in::text').get().strip()
        overview = response.css('div.article__text__overview').css('span::text').get()
        if overview:
            overview = overview.strip()
        text = response.css('div.article__text').xpath('//p//text()').getall()
        if text:
            text = ' '.join(t.strip() for t in text)
        picture_link = response.css('div.article__main-image__wrap').css('img::attr(src)').get()
        infogr = response.css('div.g-mobile-visible').css('div.article__picture__wrap').css('img::attr(src)').getall()
        authors = response.css('span.article__authors__author__name::text').getall()
        res = dict(
            date=date,
            category=category,
            title=title,
            overview=overview,
            text=text,
            link=response.request.url,
            picture=picture_link,
            infogr=infogr,
            authors=authors,
            source=self.source
        )
        yield res
