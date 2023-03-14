import scrapy


class ArticleItem(scrapy.Item):
    """Item для статьи."""
    date = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    overview = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()
    picture_link = scrapy.Field()
    video_link = scrapy.Field()
    infographic_links = scrapy.Field()
    authors = scrapy.Field()
    source = scrapy.Field()
