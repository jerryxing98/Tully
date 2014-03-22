from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from bookmark import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='bookmark_idx'),
    #timeline hot list
    url(r'^hot/$', views.hot, name='bookmark_hot'),
    #timeline recommend list
    url(r'^recommend/$', views.recommend, name='bookmark_recommend'),
    #timeline last list
    url(r'^last/$', views.last, name='bookmark_last'),
    #timeline random list
    url(r'^random/$', views.random, name='bookmark_random'),
    #timeline all tags list
    #url(r'^tags/$', views.tags, name='bookmark_tags'),
    url(r'^bk/new/$', views.new, name='bookmark_new'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.tag, name='bookmark_tag'),
    url(r'^bk/(?P<pk>\d+)/delete/$', views.delete, name='bookmark_delete'),
    url(r'^bk/(?P<pk>\d+)/postcomment_/$', views.postcomment_, name='bookmark_postcomment_'),
    url(r'^bk/(?P<pk>\d+)/$', views.detail, name='bookmark_detail'),
    url(r'^bk/(?P<pk>\d+)/edit/$', views.edit, name='bookmark_edit'),
)


