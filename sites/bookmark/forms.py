# -*- coding: UTF-8 -*-
import re

from django.core.exceptions import ValidationError

from bootstrap.forms import BootstrapModelForm
from django.forms import URLField,TextInput
#from .widgets import ImageClearableFileInput
from django import forms 
from django.conf import settings 
from django.utils.safestring import mark_safe 
from django.template.loader import render_to_string 
from django.template import RequestContext 
from django.utils.translation import ugettext_lazy as _
from bookmark.models import Bookmark, BKComment

def endsWith(s, *endings):
    return anyTrue(s.endswith, endings)

'''
def ULink(forms.URLField):
    def __init__(self,attrs={}):
        super(ULink,self).__init__(attrs)
    def render(self,name,value,attrs=None):
        rendered=supper(ULink,self).render(name,vlaue,attrs)
        context={
        }
        return rendered + mark_safe(render_to_string('bookmark/widgets/ulink.html',context))
'''
class BookmarkForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = (('draft', u'草稿'), ('pub', u'发布'), )
        self.fields['shared'].choices = ((1,u'分享'),(0,u'个人'), )
        self.fields['mtype'].choices = ((1,'HTML'),(2,'IMAGE'),(3,'TEXT'),(4,'VIDEO'),(5,'AUDIO'),)
        #self.fields['autolink'].field = forms.URLField(label='links',widget=ULink()) 
    #def clean_



    class Meta:
        model = Bookmark
        fields = ['title','link','description', 'tags','shared','mtype', 'status']
        #widgets = { 'cover': ImageClearableFileInput(), }
        widgets = {'link':TextInput(attrs={'size':64,'value':'http://'})}
        custom_fields = {'link': 'bookmark/widgets/ulink.html'}

    def save(self, created_by=None):
        if not self.instance.pk:#if new
            self.instance.created_by = created_by
        self.instance.update_updated_on(commit=False)
        #NOTE if commit=False save Tag will fail
        bookmark = super(BookmarkForm, self).save()
        return bookmark
        
def valid_date(s):
    if not s:
        return
    fmts = ['^-{0,1}\d{1,4}-\d{1,2}-\d{1,2}$', '^-{0,1}\d{1,4}-\d{1,2}$', '^-{0,1}\d{1,4}$']
    for fmt in fmts:
        if re.search(fmt, s):
            return
    raise ValidationError(u'无法识别该日期格式')



class BKCommentForm(BootstrapModelForm):
    class Meta:
        model = BKComment
        fields = ['content', ]



