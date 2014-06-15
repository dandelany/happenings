# Scrapy settings for bowerypresents project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bowerypresents'

SPIDER_MODULES = ['bowerypresents.spiders']
NEWSPIDER_MODULE = 'bowerypresents.spiders'

EXTENSIONS = {
    'scrapy.contrib.throttle.AutoThrottle': 500
}

ITEM_PIPELINES = {
    'bowerypresents.pipelines.AddToMongoDBPipeline': 300
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bowerypresents (+http://www.yourdomain.com)'
