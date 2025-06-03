BOT_NAME = "jj_scraper"

SPIDER_MODULES = ["jj_scraper.spiders"]
NEWSPIDER_MODULE = "jj_scraper.spiders"

# Configure logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Disable stats collection
STATS_DUMP = False

# Configure item pipelines
ITEM_PIPELINES = {
    'jj_scraper.pipelines.firebase_pipeline.FirebasePipeline': 300,
}

# Configure a download delay
DOWNLOAD_DELAY = 2

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 1

# Disable default logging
LOG_ENABLED = True
LOG_STDOUT = False
LOG_FILE = None

# Custom settings for cleaner output
FEED_EXPORT_ENCODING = 'utf-8'
FEEDS = {
    None: {
        'format': None,  # Disable default feed export
    }
}
