#coding=utf-8
'''
Created on 2012-2-1

@author: Chine
'''
from django.contrib.syndication.views import Feed

from models import Article

class RSSFeed(Feed):    
    title = u"翻墙乐趣的博客"
    description = "Stay Hungry,Stay Foolish..."
    link = "/"
    
    def items(self):
        return Article.completed_objects.all().order_by("-created")[:10]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract