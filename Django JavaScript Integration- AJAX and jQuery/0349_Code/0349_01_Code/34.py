if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
      (r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:],),  'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)
