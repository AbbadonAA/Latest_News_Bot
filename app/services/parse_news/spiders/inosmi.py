import scrapy
from ..items import ArticleItem
from ..settings import STANDART_CATEGORIES


class InosmiSpider(scrapy.Spider):
    name = "inosmi_spider"
    allowed_domains = ["inosmi.ru"]
    start_urls = ["http://inosmi.ru/"]

    def parse(self, response):
        pass

    def parse_theme(self, response):
        ...

    def parse_article(self, response):
        ...
