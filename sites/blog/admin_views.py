#coding=utf-8
'''
Created on 2012-9-9

@author: Chine
'''

import time
import urllib2
import urllib

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from models import BlogUser
from social.weibo import get_blog_user

@login_required
@staff_member_required
def check_weibo_auth(request):
    blog_user = BlogUser.objects.get(user=request.user)
    if not blog_user.weibo_access_token or not blog_user.weibo_access_token_expires:
        return HttpResponse("0")
    if blog_user.weibo_access_token_expires <= time.time():
        return HttpResponse("0")
    try:
        get_blog_user({'access_token': blog_user.weibo_access_token,
                       'expires': blog_user.weibo_access_token_expires,
                       'uid': blog_user.weibo_uid})
    except urllib2.HTTPError, e:
        if e.code == 403:
            return HttpResponse("0")
    return HttpResponse("1")

@login_required
@staff_member_required
def admin_weibo_auth(request):
    weibo_auth_url = '%s?%s' % (settings.WEIBO_AUTH_ENDPOINT,
                             urllib.urlencode({
                                               'response_type': 'code',
                                               'client_id': settings.WEIBO_API['app_key'],
                                               'redirect_uri': settings.WEIBO_REDIRECT_URI,
                                               }))    
    request.session['redirect_uri'] = '%s/admin/weibo/auth/done/' % settings.SITE
    
    return HttpResponseRedirect(weibo_auth_url)

@login_required
@staff_member_required
def admin_weibo_auth_deal(request):
    blog_user = BlogUser.objects.get(user=request.user)
    data = request.session['blog_user']
    blog_user.weibo_access_token = data['access_token']
    blog_user.weibo_access_token_expires = data['expires']
    blog_user.weibo_uid = data['uid']
    blog_user.save()
    del request.session['blog_user']
    return HttpResponse('''<!DOCTYPE html>
        <head>
            <script type="text/javascript" charset="utf-8">
                window.close();
            </script>
        </head>
    </html>''')