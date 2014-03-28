# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from ebook import models
from ebook import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='product_idx'),    #timeline hot list
    url(r'^hot/$', views.hot, name='product_hot'),
    #timeline recommend list
    url(r'^recommend/$', views.recommend, name='product_recommend'),
    #timeline last list
    url(r'^last/$', views.last, name='product_last'),
    #timeline random list
    url(r'^random/$', views.random, name='product_random'),
    #timeline all tags list
    #url(r'^tags/$', views.tags, name='bookmark_tags'),
    url(r'^pd/new/$', views.new, name='product_new'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.tag, name='product_tag'),
    url(r'^pd/(?P<pk>\d+)/delete/$', views.delete, name='product_delete'),
    #url(r'^bk/(?P<pk>\d+)/postcomment_/$', views.postcomment_, name='product_postcomment_'),
    url(r'^pd/(?P<pk>\d+)/$', views.detail, name='product_detail'),
    url(r'^pd/(?P<pk>\d+)/edit/$', views.edit, name='product_edit'),
    url(r'^tags/$', views.tags, name='product_tags'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.tag, name='product_tag'),
)
