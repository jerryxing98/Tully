#coding=utf-8
'''
Created on 2012-1-28

@author: Chine
完成邮件的订阅功能，主要模块:1.分类显示，2.评论  3.TAG 4.RSS  5.sitemap
'''

from django.conf.urls.defaults import *

from sitemap import ArticleSitemap
from feeds import RSSFeed

urlpatterns = patterns('blog.views',
    # Index page
    url(r'^$', 'index', name='blog_index'),
    url(r'^page/(?P<page>\d+)/$', 'index', name="blog_index_pages"),
    # Article page
    url(r'^article/(?P<slug>[-\w]+)/$', 'article', name='blog_article'),
    # Category page
    url(r'^category/$', 'categories', name='blog_categories'),
    url(r'^category/(?P<slug>\w+)/$', 'category', name='blog_category'),
    url(r'^category/(?P<slug>\w+)/page/(?P<page>\d+)/$', 'category', name='blog_category_pages'),
    # Contact
    url(r'^contact/$', 'contact', name='blog_contact'),
    # About
    url(r'^about/$', 'about', name='blog_about'),
    # Tag
    url(r'^tag/(?P<slug>[-\w]+)/$', 'tag', name='blog_tag'),
    url(r'^tag/(?P<slug>[-\w]+)/page/(?P<page>\d+)/$', 'tag', name='blog_tag_pages'),
    # Comment
    url(r'^comment/add/$', 'comment', name='blog_comment'),
    # Comments(ajax)
    url(r'^comment/(?P<slug>[-\w]+)/$', 'comments', name='blog_article_comments'),
    # Search
    url(r'^search/$', 'search', name='blog_search'),
    url(r'^search/page/(?P<page>\d+)/$', 'search', name='blog_search_pages'),
    # Subscriber
    url(r'^subscriber/add/$', 'subscriber', name='blog_subscriber'),
    # Unsubscribe
    url(r'^subscribe/cancel/$', 'unsubscriber', name='blog_unsubscriber')
)

# rss
urlpatterns += patterns('',
    url(r'^rss/$', RSSFeed(), name='blog_rss'),
    #url(r'^article/(?P<slug>[-\w]+)/rss/$', ArticleFeed, name='program-article-rss'),
)

# Sitemap
sitemaps = {  
    'article': ArticleSitemap,       
}
urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), 
)