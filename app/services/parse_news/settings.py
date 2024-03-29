import sys

# Необходимо для запуска паука вручную (иначе не видит импорты из app)
sys.path.append('/home/abbadon/dev/Latest_News_Bot/')
sys.path.append('/LATEST_NEWS_BOT/')

BOT_NAME = "parse_news"

SPIDER_MODULES = ["parse_news.spiders"]
NEWSPIDER_MODULE = "parse_news.spiders"

ROBOTSTXT_OBEY = True

LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   "app.services.parse_news.pipelines.ArticlesToDBPipeline": 300,
}

TELNETCONSOLE_ENABLED = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
STANDART_CATEGORIES = {
    'Спорт': 'Спорт',
    'Политика': 'Политика',
    'Экономика': 'Экономика',
    'Бизнес': 'Экономика',
    'Финансы': 'Экономика',
    'Крипто': 'Экономика',
    'Общество': 'Общество',
}
