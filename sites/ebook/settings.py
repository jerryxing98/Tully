from django.conf import settings
gettext = lambda s: s

#thumbnaler defailt size 
EBOOK_THUMBNAIL_SIZE = getattr(settings,
                               'EBOOK_THUMBNAIL_SIZE',
                               140)
#thumbnail crop size
EBOOK_THUMBNAIL_CROP_TYPE = getattr(settings,
                                    'EBOOK_THUMBNAIL_CROP_TYPE',
                                    'smart')



EBOOK_THUMBNAIL_PATH = getattr(settings,
		                       'EBOOK_THUMBNAIL_PATH', 
		                       '/thumbnail')

#if the thumbnail path can't found ,use this path instead
EBOOK_THUMBNAIL_URL = getattr(settings,
		                       'EBOOK_THUMBNAIL_URL', 
		                       '/static/img/tl-default-small.gif')
