#coding=utf-8
'''
Created on 2012-2-8

@author: Chine
'''

from django import forms
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType

from models import Comment, Subscriber

#评论者的邮箱
class CommentForm(ModelForm):
    username = forms.CharField(
                    widget=forms.TextInput(attrs={
                                                  'id': 'name',
                                                  'value': '你的昵称',
                                                  'tabindex': '1',
                                                  'onfocus': "inputFocusOrBlur(this, 0, '你的昵称');",
                                                  'onblur': "inputFocusOrBlur(this, 1, '你的昵称');"
                                                  }), max_length=50)
    email_address = forms.EmailField(
                    widget=forms.TextInput(attrs={
                                                  'id': 'email',
                                                  'value': '你的邮箱',
                                                  'tabindex': '2',
                                                  'onfocus': "inputFocusOrBlur(this, 0, '你的邮箱');",
                                                  'onblur': "inputFocusOrBlur(this, 1, '你的邮箱');"
                                                  }), max_length=75)
    site = forms.URLField(
                    widget=forms.TextInput(attrs={
                                                  'id': 'website',
                                                  'value': '你的网站',
                                                  'tabindex': '3',
                                                  'onfocus': "inputFocusOrBlur(this, 0, '你的网站');",
                                                  'onblur': "inputFocusOrBlur(this, 1, '你的网站');"
                                                  }), required=False, max_length=200)
    content = forms.CharField(
                    widget=forms.Textarea(attrs={
                                                  'id': 'message',
                                                  'rows': '10',
                                                  'cols': '18',
                                                  'tabindex': '4',
                                                  }))
    
    # Hidden Input
    avatar = forms.URLField(widget=forms.HiddenInput, required=False)
    reply_to_comment = forms.ModelChoiceField(Comment.objects.all(), widget=forms.HiddenInput(), required=False)
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Comment

#订阅者的邮箱
class SubscriberForm(ModelForm):
    username = forms.CharField(
                    widget=forms.TextInput(attrs={
                                                  'id': 'name',
                                                  'value': '你的昵称',
                                                  'onfocus': "inputFocusOrBlur(this, 0, '你的昵称');",
                                                  'onblur': "inputFocusOrBlur(this, 1, '你的昵称');"
                                                  }), max_length=50)
    email_address = forms.EmailField(
                    widget=forms.TextInput(attrs={
                                                  'id': 'email',
                                                  'value': '你的邮箱',
                                                  'onfocus': "inputFocusOrBlur(this, 0, '你的邮箱');",
                                                  'onblur': "inputFocusOrBlur(this, 1, '你的邮箱');"
                                                  }), max_length=75)
    
    class Meta:
        model = Subscriber