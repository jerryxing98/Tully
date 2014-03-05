# -*- coding: UTF-8 -*-
from django import forms
from models import *
from bootstrap.forms import BootstrapModelForm
from .models import *



class ProductForm(BootstrapModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = (('draft', u'草稿'), ('pub', u'发布'), )
        #self.fields['shared'].choices = ((1,u'分享'),(2,u'隐私'), )

    class Meta:
        model = Product
        fields = ['title','description','price', 'thumbnail','tags', 'status']
        #widgets = { 'cover': ImageClearableFileInput(), }

    def save(self, created_by=None):
        if not self.instance.pk:#if new
            self.instance.created_by = created_by
        self.instance.update_updated_on(commit=False)
        #NOTE if commit=False save Tag will fail
        product = super(ProductForm, self).save()
        return product
        



def valid_date(s):
    if not s:
        return
    fmts = ['^-{0,1}\d{1,4}-\d{1,2}-\d{1,2}$', '^-{0,1}\d{1,4}-\d{1,2}$', '^-{0,1}\d{1,4}$']
    for fmt in fmts:
        if re.search(fmt, s):
            return
    raise ValidationError(u'无法识别该日期格式')


