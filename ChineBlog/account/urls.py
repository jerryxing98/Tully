#-*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from userena import views as userena_views

from account.forms import BsSignupForm
from account.forms import BsAuthenticationForm
from account.forms import BsEditProfileForm
from account.forms import BsPasswordChangeForm
from account.forms import BsChangeEmailForm 

urlpatterns = patterns('',
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
    (r'^', include('userena.urls')),
)

