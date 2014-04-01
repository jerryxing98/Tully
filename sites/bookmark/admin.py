from django.contrib import admin
from bookmark.models import Bookmark,Link

'''
	ProductModel show in djangoAdmin
'''
class BookmarkAdmin(admin.ModelAdmin):

    list_display        = ('title', 'status', 'description', 'mtype', 'shared', 'thumbnail')
    search_fields       = ('title', 'description')
    #raw_id_fields       = ('attachments', 'created_by')


class LinkAdmin(admin.ModelAdmin):
    list_display =('url','image')
    search_fields=('url','image')
    


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Link, LinkAdmin)

