from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import logging

from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models import F
from bookmark.models import Bookmark
from timeline.models import Timeline
from ebook.models import Product
from timeline.models import Timeline
from ebook.models import Product



class Favorite(models.Model):
    user = models.ForeignKey('auth.User')
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    


def autoPlusFavorite(sender,**kwargs):
    instance = kwargs.get('instance')
    if instance.target_content_type.model  == 'timeline':
        timeline = Timeline.objects.get(id = instance.target_object_id)
        timeline.num_favorites = F("num_favorites")+1
        timeline.save()
    if instance.target_content_type.model  == 'bookmark':
        bookmark = Bookmark.objects.get(id = instance.target_object_id)
        bookmark.num_favorites = F("num_favorites")+1
        bookmark.save()
    if instance.target_content_type.model  == 'product':
        product = Product.objects.get(id = instance.target_object_id)
        product.num_favorites = F("num_favorites")+1
        product.save()

def autoReduceFavorite(sender,**kwargs):
    instance = kwargs.get('instance')
    if instance.target_content_type.model  == 'timeline':
        timeline = Timeline.objects.get(id = instance.target_object_id)
        timeline.num_favorites = F("num_favorites")-1
        timeline.save()
    if instance.target_content_type.model  == 'bookmark':
        bookmark = Bookmark.objects.get(id = instance.target_object_id)
        bookmark.num_favorites = F("num_favorites")-1
        bookmark.save()
    if instance.target_content_type.model  == 'product':
        product = Product.objects.get(id = instance.target_object_id)
        product.num_favorites = F("num_favorites")-1
        product.save()

post_save.connect(autoPlusFavorite,sender=Favorite)
post_delete.connect(autoReduceFavorite,sender=Favorite)
    
