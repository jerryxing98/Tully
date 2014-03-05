#!/usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from filebrowser.sites import site
from django.conf.urls.static import static
from userena.contrib.umessages import views as messages_views
from account.forms import BsComposeForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()




urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChineBlog.views.home', name='home'),
    # url(r'^ChineBlog/', include('ChineBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/check_weibo_auth/$', 'blog.admin_views.check_weibo_auth'),
    url(r'^admin/weibo/auth/$', 'blog.admin_views.admin_weibo_auth'),
    url(r'^admin/weibo/auth/done/$', 'blog.admin_views.admin_weibo_auth_deal'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^messages/compose/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_compose'),
    url(r'^messages/compose/(?P<recipients>[\+\.\w]+)/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_compose_to'),
    url(r'^messages/reply/(?P<parent_id>[\d]+)/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_reply'),
    url(r'^messages/', include('userena.contrib.umessages.urls')),

    #url(r'^attachments/', include('attachments.urls')),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), 
      name="jerryminds_about"),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"),
      name="jerryminds_faq"),
)


#sitemap
'''
urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
'''

# Grappelli url mapping
urlpatterns += patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
)

# Accounts
urlpatterns += patterns('',
    (r'^accounts/', include('social.urls')),
    (r'^account/',include('account.urls'))
)
    
# Blog
urlpatterns += patterns('',
    (r'^blog/', include('blog.urls'))
)

# Bookmark
urlpatterns += patterns('',
    (r'^bookmark/',include('bookmark.urls'))
)

#====================================
#the friend model
#====================================
'''
urlpatterns += patterns('',
		url(r'^friend/',include('friend.urls')),
		)
'''
#

#timeline

urlpatterns += patterns('',
    (r'^timeline/',include('timeline.urls'))
)

urlpatterns += patterns ('',
 (r'^ebook/', include('ebook.urls')),
)


# Static files url if DEBUG

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

