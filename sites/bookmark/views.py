# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from guardian.shortcuts import assign, remove_perm, get_users_with_perms
from taggit.models import Tag

from ajax_validation.views import validate_form
from ajax_validation.utils import render_json_response
from ajax_validation.utils import render_string

from attachments.views import _do_ajax_upload, ajax_delete, ajax_change_descn 
from attachments.models import Attachment

from .models import Bookmark
from .forms import BookmarkForm, BKCommentForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage



def index(request):
  return recommend(request)


def hot(request, template_name="bookmark/bookmarks.html"):
    ctx = {}
    ctx['pg'] = 'hot'
    ctx['bookmarks'] = Bookmark.objects.get_hot_bookmarks()
    return render(request, template_name, ctx)


def last(request, template_name="bookmark/bookmarks.html"):
    ctx = {}
    ctx['pg'] = 'last'
    ctx['bookmarks'] = Bookmark.objects.get_last_bookmarks()
    return render(request, template_name, ctx)


def recommend(request, template_name="bookmark/bookmarks.html"):
    ctx = {}
    ctx['pg'] = 'recommend'
    ctx['bookmarks'] = Bookmark.objects.get_recommend_bookmarks()
    return render(request, template_name, ctx)


def random(request, template_name="bookmark/bookmarks.html"):
    ctx = {}
    ctx['pg'] = 'random'
    ctx['bookmarks'] = Bookmark.objects.get_random_bookmarks()
    return render(request, template_name, ctx)

def tags(request, template_name="timeline/tags.html"):
    ctx = {}
    return render(request, template_name, ctx)


def tag(request, tag_name, template_name="bookmark/bookmarks.html"):
    ctx = {}
    ctx['pg'] = 'tag'
    ctx['tag'] = get_object_or_404(Tag, name=tag_name)
    bookmarks = Bookmark.objects.get_tag_bookmarks(tag_name) 
    ctx['bookmarks'] = bookmarks
    return render(request, template_name, ctx)


def detail(request, pk, template_name="bookmark/detail.html"):
    ctx = {}
    bookmark = get_object_or_404(Bookmark, pk=pk)
    bookmark.num_views += 1
    bookmark.save()
    ctx['bm'] = bookmark
    ctx['user'] = bookmark.created_by
    if bookmark.created_by==request.user:
        ctx['auth_can_edit'] = True 
    ctx['comments'] = bookmark.bkcomment_set.order_by('created_on')
    ctx['form'] = BKCommentForm()
    #ctx['site'] = Site.objects.get_current()
    return render(request, template_name, ctx)

@login_required
def delete(request, pk):
    bml = get_object_or_404(Bookmark, pk=pk)
    if bml.created_by != request.user:
        return HttpResponse(u'您没有权限执行该操作')
    bml.status = 'del'
    bm1.save()
    return redirect('bookmark_idx')

def postcomment_(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    form, validate = validate_form(request, form_class=BKCommentForm)
    if not request.user.is_authenticated():
        return render_json_response({'valid': False})
    if validate['valid']:
        c = form.save(commit=False)
        c.bookmark = bookmark
        c.created_by = request.user
        c.save()
        bookmark.update_num_replies()
        validate['html'] = render_to_string('bookmark/inc_comment.html', { 'c': c })
    return render_json_response(validate)


@login_required
def new(request):
    ctx = {}
    template_name = 'bookmark/form.html'
    form = BookmarkForm()
    if request.method == "POST":
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(created_by=request.user)
            return redirect('bookmark_last', bookmark.pk)
    ctx['form'] = form
    return render(request, template_name, ctx)


@login_required
def edit(request, pk):
    ctx = {}
    template_name = 'bookmark/form.html'
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if not bookmark.created_by==request.user:
        return HttpResponse(u'您没有权限执行该操作')
    ctx['bml'] = bookmark
    form = BookmarkForm(instance=bookmark)
    if request.method == "POST":
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            messages.info(request, u'成功编辑')
            return redirect('bookmark_detail', bookmark.pk)
    ctx['form'] = form
    ctx['bml'] = bookmark
    return render(request, template_name, ctx)




def get_pagination_page(page=1):
    items = range(0, 100)
    paginator = Paginator(items, 2)
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return items