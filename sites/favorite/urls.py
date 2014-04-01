from django.conf.urls import patterns, url
from favorite.views import add_or_remove


urlpatterns = patterns('',
    url(r'^add-or-remove$', 'add_or_remove',name="add_or_remove"),
)
