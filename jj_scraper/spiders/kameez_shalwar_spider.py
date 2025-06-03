import scrapy
from jj_scraper.items import JjScraperItem
import logging

class KameezShalwarSpider(scrapy.Spider):
    name = "kameez_shalwar"
    allowed_domains = ["junaidjamshed.com"]
    start_urls = ["https://www.junaidjamshed.com/mens/kameez-shalwar.html"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")
        
        products = response.css('li.item.product.product-item')
        self.logger.info(f"Found {len(products)} products on page")

        for product in products:
            item = JjScraperItem()
            
            item['product_id'] = product.css('::attr(data-product-id)').get()
            item['name'] = product.css('a.product-item-link::text').get()
            if item['name']:
                item['name'] = item['name'].strip()
            
            item['price'] = product.css('span.price::text').get()
            item['availability'] = 'In Stock' if not product.css('div.stock.unavailable') else 'Out of Stock'
            item['url'] = product.css('a.product-item-link::attr(href)').get()
            item['image_url'] = product.css('img.product-image-photo::attr(data-original)').get()
            
            yield item

        # Find next page URL dynamically
        next_page = response.css('a.action.next::attr(href)').get()
        if next_page:
            self.logger.info(f"Found next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("No more pages found")
