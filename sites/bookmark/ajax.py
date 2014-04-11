# -*- coding: UTF-8 -*-
from dajaxice.decorators import dajaxice_register
from bookmark.views import recommend
from django.template import RequestContext, loader
from bookmark.forms import BKCommentForm
from account.ajax import ajax_login
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from bookmark.views import recommend
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404
from bookmark.forms import BKCommentForm
from django.contrib.auth import login,authenticate,logout
from account.forms import BsAuthenticationForm
from userena.forms import SignupForm,SignupFormOnlyEmail,AuthenticationForm,ChangeEmailForm,EditProfileForm
from dajaxice.utils import deserialize_form
from  django.shortcuts import render_to_response
from bookmark.models import Bookmark
from ajax_validation.views import validate_form
from thummer import get_thumbnail
from thummer.models import WebpageSnapshot

@dajaxice_register(method='GET')
def ajax_recommend(request,page):
    html= recommend(request, template_name="authapi/bookmarks.html")    
    return simplejson.dumps({'message':html.content})

@dajaxice_register(method='POST',name='bookmark.ajax_screenshot')
def ajax_screenshot(request,url):
    if request.method=='POST':
        try:
            thumbnail = get_thumbnail(url, '400x400')
            status='Success'
            #thumbnail = get_object_or_404(WebpageSnapshot, url=url)
            print "image.url===================",str(thumbnail)
            message=[url,str(thumbnail)]
        except:
            status='Fail'
            message=[url,'errors:the image capture errors!']
        return simplejson.dumps({'status':status,'message':message})


@dajaxice_register(method='GET',name='bookmark.ajax_comment_get')
@dajaxice_register(method='POST',name='bookmark.ajax_comment_post')
def ajax_comment(request,form,pk):
    if request.method =='POST':
        form=BKCommentForm(deserialize_form(form))
        bookmark = get_object_or_404(Bookmark, pk=pk)
        if form.is_valid():
            c = form.save(commit=False)
            c.bookmark = bookmark
            c.created_by = request.user
            c.save()
            bookmark.update_num_replies()
            num_replies=bookmark.num_replies
            return simplejson.dumps({'status':'Success','message':[bookmark.pk,num_replies]})
        else:
            #dajax.remove_css_class('#signin_form input', 'error')
            #for error in form.errors:
            #    dajax.add_css_class('#id_%s' % error, 'error')
            html = render(request, 'authapi/comment.html', {'form':form,'bk':bookmark})
            return simplejson.dumps({'status':'Error','message':html.content})
    
    if request.method == 'GET':
        if request.user.is_authenticated():
            bookmark = get_object_or_404(Bookmark, pk=pk)
            form = BKCommentForm()
            html = render(request, 'authapi/comment.html', {'form':form,'bk':bookmark})
            return simplejson.dumps({'message':html.content})    
        else:
            request.session['Tip']=u'   you are anonymous,Please login!'
            return ajax_login(request,form)



