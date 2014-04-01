#coding=utf-8
'''
Created on 2012-2-1

@author: Chine
'''
from django.contrib.syndication.views import Feed

from bookmark.models import Bookmark
from ebook.models import Product
from timeline.models import Timeline



class FeedModel(object):
	def __init__(self,title,abstract):
		self.title=title
		self.abstract=abstract
	


class RSSFeed(Feed):    
    title = u"翻墙乐趣"
    description = "Stay Hungry,Stay Foolish..."
    link = "/"
    
    def items(self):
    	lists =  []
    	'''
    	bookmarks = Bokkmark.objects.all().order_by("-created")[:10]
        ebooks = Product.objects.all().order_by("-created")[:10]
        timeline = Timeline.objects.all().order_by("-created")[:10]
        lists.extend(bookmarks).extend(timeline).extend(ebooks)
        '''
        return Bookmark.objects.all().order_by("-created_on")[:10]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract