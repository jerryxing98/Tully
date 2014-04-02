# Scrapy settings for crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
'''
BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'
'''
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlers (+http://www.yourdomain.com)'
# Scrapy settings for crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlers (+http://www.yourdomain.com)'

import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'settings'))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings") #Changed in DDS v.0.3

BOT_NAME = 'ebook'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'ebook.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

ITEM_PIPELINES = [
    'dynamic_scraper.pipelines.ValidationPipeline',
    'ebook.scraper.pipelines.DjangoWriterPipeline',
]