from django.contrib import admin
from ebook.models import Product

'''
	ProductModel show in djangoAdmin
'''
class ProductAdmin(admin.ModelAdmin):

    list_display        = ('thumbnail', 'created_by', 'status', 'num_views', 'num_replies', )
    search_fields       = ('title', 'created_by__username', )
    #raw_id_fields       = ('attachments', 'created_by')

admin.site.register(Product, ProductAdmin)
