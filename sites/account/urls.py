#-*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from userena import views as userena_views

from account.forms import BsSignupForm
from account.forms import BsAuthenticationForm
from account.forms import BsEditProfileForm
from account.forms import BsPasswordChangeForm
from account.forms import BsChangeEmailForm 
from django.views.generic.simple import direct_to_template
from account.views import friends,follow,remove_follow
from account.views import authapi_signin




urlpatterns = patterns('',
    #   name='userena_profile_list'),
    url(r'^signup/$', userena_views.signup,
        {'signup_form': BsSignupForm}, name='userena_signup'),
    url(r'^signin/$', userena_views.signin,
        {'auth_form': BsAuthenticationForm}, name='userena_signin'),
    url(r'^(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit,
       {'edit_profile_form': BsEditProfileForm}, name='userena_profile_edit'),
    # Change password
    url(r'^(?P<username>[\.\w]+)/password/$',
       userena_views.password_change,
       {'pass_form': BsPasswordChangeForm}, name='userena_password_change'),
    url(r'^(?P<username>[\.\w]+)/email/$',
       userena_views.email_change,
       {'email_form': BsChangeEmailForm}, name='userena_email_change'),
    #url(r'^friend/list/(?P<username>[\.\w]+)/(?P<ftype>[\.\w]+)$',
    #  direct_to_template,
    #  {'template':'friends.html'},
    #name = 'friend_list'),
    url(r'^friend/list/(?P<username>[\.\w]+)/(?P<ftype>[\.\w]+)$',
        friends,
        name='friend_list'),
    #url(r'',)
    url(r'^friend/follows$',follow,name = 'friend_follows'),
    url(r'^friend/follows/delete$',remove_follow,name = 'friend_delete_follows'),
    #url(r'^authapi/signup/$',authapi_signup,{'signup_form':BsSignupForm},name='authapi_signup'),
    url(r'^authapi/signin/$',authapi_signin,{'auth_form': BsAuthenticationForm},name='authapi_signin'),

    (r'^', include('userena.urls')),

)

