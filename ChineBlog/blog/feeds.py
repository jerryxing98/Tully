#coding=utf-8
'''
Created on 2012-2-1

@author: Chine
'''
from django.contrib.syndication.views import Feed

from models import Article

class RSSFeed(Feed):    
    title = u"残阳似血的博客"
    description = "Lost good things..."
    link = "/"
    
    def items(self):
        return Article.completed_objects.all().order_by("-created")[:10]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract