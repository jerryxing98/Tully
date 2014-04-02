from django.contrib import admin
from ebook.models import Product,Article,ProductWebsite

'''
	ProductModel show in djangoAdmin
'''
class ProductAdmin(admin.ModelAdmin):

    list_display        = ('thumbnail', 'created_by', 'status', 'num_views', 'num_replies', )
    search_fields       = ('title', 'created_by__username', )
    #raw_id_fields       = ('attachments', 'created_by')

class ArticleAdmin(admin.ModelAdmin):
	list_display =('created_by','status')
	search_fields = ('title','created_by__username')

class ProductWebsiteAdmin(admin.ModelAdmin):
    list_display =('name','url','scraper','scraper_runtime')
    search_fields =('name','url')
    

admin.site.register(Article,ArticleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductWebsite,ProductWebsiteAdmin)


