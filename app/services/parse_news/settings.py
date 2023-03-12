import sys

sys.path.append('/home/abbadon/dev/Latest_News_Bot/')

BOT_NAME = "parse_news"

SPIDER_MODULES = ["parse_news.spiders"]
NEWSPIDER_MODULE = "parse_news.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   "parse_news.pipelines.ArticlesToDBPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
