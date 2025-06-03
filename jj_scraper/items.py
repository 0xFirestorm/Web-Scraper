import scrapy

class JjScraperItem(scrapy.Item):
    product_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
