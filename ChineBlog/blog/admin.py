#coding=utf-8
'''
Created on 2012-1-21

@author: Chine
'''

from django.contrib import admin
from django.contrib.contenttypes import generic
from django import forms

from models import *
from ChineBlog.social.models import SocialItem

class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    
class CommentInline(generic.GenericStackedInline):
    model = Comment
    
class SocialItemInline(generic.GenericStackedInline):
    model = SocialItem
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')

class TagAdmin(admin.ModelAdmin):
    inlines = (ArticleTagInline,)
    prepopulated_fields = {"slug": ("name",)}
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email_address', 'site', 'content', 'avatar', 'ip', 'visible', 'post_date', 'comment_obj',)
    list_per_page = 10
    inlines = (SocialItemInline, )
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_always_above', 'status', 'clicks', 'created', 'modified')
    list_filter = ('status', 'created', 'modified')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }
    fieldsets = [
        ('文章编辑', {'fields': ('title', 'slug', 'content',)}),
        ('日期', {'fields': ('created', 'modified')}),
        ('信息', {'fields': ('category', 'author', 'status', 'is_always_above', 'share')}),
    ]
    readonly_fields = ("created",)
    inlines = (ArticleTagInline, CommentInline, SocialItemInline)
    list_per_page = 10
    ordering = ['-created']
    
    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
               '/static/grappelli/tinymce_setup/tinymce_setup.js',)
        
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'small_avatar', 'info' )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor'})},
    }    
    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
               '/static/grappelli/tinymce_setup/tinymce_setup.js',)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')
    
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email_address', 'enabled')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(BlackList)
admin.site.register(Subscriber, SubscriberAdmin)