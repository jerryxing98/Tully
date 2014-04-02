# Scrapy settings for open_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os
import imp

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#imp.find_module('settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


BOT_NAME = 'ebook'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'ebook.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

ITEM_PIPELINES = [
    'dynamic_scraper.pipelines.DjangoImagesPipeline',
    'dynamic_scraper.pipelines.ValidationPipeline',
    'ebook.scraper.pipelines.DjangoWriterPipeline',
]

IMAGES_STORE = os.path.join(PROJECT_ROOT, '../thumbnails')

IMAGES_THUMBS = {
    'small': (170, 170),
}

DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'INFO'
DSCRAPER_LOG_LIMIT = 5