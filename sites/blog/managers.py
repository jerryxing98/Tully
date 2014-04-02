#coding=utf-8
'''
Created on 2012-2-1

@author: Chine
'''

from django.db import models
from django.db.models import Q

from mptt.managers import TreeManager

class CompletedArticleManager(models.Manager):
    def get_query_set(self):
        return super(CompletedArticleManager, self).get_query_set().filter(status=2)
    
class CommentToArticleManager(TreeManager):
    def get_query_set(self):
        return super(CommentToArticleManager, self)\
            .get_query_set()\
            .filter(Q(visible=True) & Q(content_type__model="article"))
            
class CommentsVisibleManager(models.Manager):
    def get_query_set(self):
        return super(CommentsVisibleManager, self)\
            .get_query_set()\
            .filter(visible=True)\

class CommentToBlogUserManager(TreeManager):
    def get_query_set(self):
        return super(CommentToBlogUserManager, self)\
            .get_query_set()\
            .filter(Q(visible=True) & Q(content_type__model="bloguser"))
            
class EnabledSubscriberManager(models.Manager):
    def get_query_set(self):
        return super(EnabledSubscriberManager, self).get_query_set().filter(enabled=True)