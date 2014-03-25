import django.contrib.admin
import directory.models
import tagging

django.contrib.admin.autodiscover()
django.contrib.admin.site.register(directory.models.Entity)
django.contrib.admin.site.register(directory.models.Location)
tagging.register(directory.models.Entity)
