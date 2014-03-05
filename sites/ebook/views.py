# -*- coding: UTF-8 -*-
# Create your views here.
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect

# app specific files

from .models import *
from .forms import *




def hot(request, template_name="ebook/products.html"):
    ctx = {}
    ctx['pg'] = 'hot'
    ctx['products'] = Product.objects.get_hot_products()
    return render(request, template_name, ctx)

def last(request, template_name="ebook/products.html"):
    ctx = {}
    ctx['pg'] = 'last'
    ctx['products'] = Product.objects.get_last_products()
    return render(request, template_name, ctx)

def recommend(request, template_name="ebook/products.html"):
    ctx = {}
    ctx['pg'] = 'recommend'
    ctx['products'] = Product.objects.get_recommend_products()
    return render(request, template_name, ctx)

def random(request, template_name="ebook/products.html"):
    ctx = {}
    ctx['pg'] = 'random'
    ctx['products'] = Product.objects.get_random_products()
    return render(request, template_name, ctx)

def tag(request, tag_name, template_name="ebook/products.html"):
    ctx = {}
    ctx['pg'] = 'tag'
    ctx['tag'] = get_object_or_404(Tag, name=tag_name)
    products = Product.objects.get_tag_products(tag_name) 
    ctx['products'] = products
    return render(request, template_name, ctx)


#@login_required
def new(request):
    form = ProductForm(request.POST or None)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            pd1 = form.save(created_by=request.user)
            return redirect('product_last')
    t = get_template('ebook/form.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def index(request):
  
    products = Product.objects.all()
    paginator = Paginator(products ,10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('ebook/products.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def detail(request, pk):
    pdl = get_object_or_404(Product, pk=pk)
    t=get_template('ebook/view_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required
def delete(request, pk):
    pdl = get_object_or_404(Product, pk=pk)
    if pd1.created_by != request.user:
        return HttpResponse(u'您没有权限执行该操作')
    pd1.status = 'del'
    pd1.save()
    return redirect('product_idx')


#@login_required
def edit(request, pk):
    pd1 = get_object_or_404(Product,pk=id)
    form = ProductForm(request.POST or None, instance = pd1)

    if form.is_valid():
        form.save()
    t=get_template('ebook/forms.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))



