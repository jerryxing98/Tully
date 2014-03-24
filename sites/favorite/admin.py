from django.contrib import admin
from favorite.models import Favorite

'''
	FavoriteModel show in djangoAdmin
'''
class FavoriteAdmin(admin.ModelAdmin):

    list_display        = ('user', 'timestamp', )
    search_fields       = ('user', 'timestamp', )
    #raw_id_fields       = ('attachments', 'created_by')

admin.site.register(Favorite, FavoriteAdmin)
