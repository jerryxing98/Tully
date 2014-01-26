#coding=utf-8
'''
Created on 2012-2-1

@author: Chine
'''

from django.contrib.sitemaps import Sitemap

from models import Article

class ArticleSitemap(Sitemap):
    changefrep = "daily"
    priority = 0.5
    
    def items(self):
        return Article.completed_objects.all()
    
    def lastmod(self, obj):
        return obj.modified