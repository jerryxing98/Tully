# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from bookmark.models import Bookmark
from bookmark.models import Link



class CrawlersItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class BookmarkItem(DjangoItem):
	django_model = Bookmark

class LinkItem(DjangoItem):
	django_model = Link



