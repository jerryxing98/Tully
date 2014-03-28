#coding=utf-8
from account.feeds import RSSFeed
from account.views import describe_email
from account.views import describe_rss
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from filebrowser.sites import site
from django.conf.urls.static import static
from userena.contrib.umessages import views as messages_views
from account.forms import BsComposeForm
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
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
      name="site_about"),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"),
      name="site_faq"),
    url(r'describe_email/$',describe_email,name="site_describe_email"),
    url(r'describe_rss/$',RSSFeed(),name="site_describe_rss"),
)


# Grappelli url mapping
urlpatterns += patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
)

# Accounts

urlpatterns += patterns('',
    (r'^accounts/', include('social.urls')),
    (r'^account/',include('account.urls')),
)


urlpatterns += patterns('',
    (r'^favorite/',include('favorite.urls'))
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
# Blog
urlpatterns += patterns('',
    (r'^blog/', include('blog.urls')),
)

# Bookmark
urlpatterns += patterns('',
    (r'^bookmark/',include('bookmark.urls')),
)
#timeline

urlpatterns += patterns('',
    (r'^timeline/',include('timeline.urls')),
)

urlpatterns += patterns ('',
 (r'^ebook/', include('ebook.urls')),
)

# Static files url if DEBUG
#sitemap
'''
urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
'''

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

