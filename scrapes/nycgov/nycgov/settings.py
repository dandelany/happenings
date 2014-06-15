# Scrapy settings for nycgov project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nycgov'

SPIDER_MODULES = ['nycgov.spiders']
NEWSPIDER_MODULE = 'nycgov.spiders'

EXTENSIONS = {
    'scrapy.contrib.throttle.AutoThrottle': 500
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_DEBUG = True

ITEM_PIPELINES = {
    'nycgov.pipelines.AddToMongoDBPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nycgov (+http://www.yourdomain.com)'
