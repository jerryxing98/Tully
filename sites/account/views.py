#-*- coding:utf-8 -*-
# Create your views here.
from userena import views as userena_views
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from friendship.models import Friend,Follow
from django.views.generic.simple import direct_to_template
from userena.views import profile_detail as __profile_detail
#from timeline.models import get_all_timlines
from userena.utils import signin_redirect, get_profile_model, get_user_model
#from userena import signals as userena_signals
from userena import settings as userena_settings
from guardian.decorators import permission_required_or_403
from userena.views import ExtraContextTemplateView
from userena.decorators import secure_required
import warnings
from django.views.generic import TemplateView
from friendship.models import Friend, Follow
from django.http import Http404, HttpResponseRedirect,QueryDict
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from feeds import RSSFeed
from userena.forms import SignupForm,SignupFormOnlyEmail,AuthenticationForm,ChangeEmailForm,EditProfileForm
from utils import render_json_response
from django.template import loader, Context
'''
class UserProfileListView(ProfileListView):
    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
'''     
def profile_detail(request, username):
    print '=========================================='
    ctx = {}
    view_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated() and request.user.username == username:
        ctx['timelines']=''
        #ctx['timelines'] = view_user.timeline_set.exclude(status='del').order_by('-updated_on')
    else:
        ctx['timelines'] = ''
        #ctx['timelines'] = get_all_timlines().filter(created_by=view_user)
    return __profile_detail(request, username, extra_context=ctx)


@secure_required
def _friends(request,username,
                 template_name='friends.html', success_url=None,
                 extra_context=None):
    user = get_object_or_404(get_user_model(),
                             username__iexact=username)
    profile = user.get_profile()
    user_initial = {'first_name': user.first_name,
                    'last_name': user.last_name}
    data = locals()
    if not extra_context: extra_context = dict()
    #extra_context['ftype'] = ftype
    extra_context['profile'] = profile
    #extra_context['user'] = user
    #more_data = {'username':username,'ftype':ftype}
    #return direct_to_template(template = 'friends.html', kwargs=kwargs)
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)

def  authapi_signin(request, auth_form=AuthenticationForm,
           template_name='authapi/signin_form.html',
           extra_context=None):
    form = auth_form()

    if request.method == 'POST':
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification, password, remember_me = (form.cleaned_data['identification'],
                                                     form.cleaned_data['password'],
                                                     form.cleaned_data['remember_me'])
            user = authenticate(identification=identification,
                                password=password)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                else: request.session.set_expiry(0)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(request, _('You have been signed in.'),
                                     fail_silently=True)

                #send a signal that a user has signed in
                userena_signals.account_signin.send(sender=None, user=user)
                # Whereto now?
                '''
                redirect_to = redirect_signin_function(
                    request.REQUEST.get(redirect_field_name), user)
                return HttpResponseRedirect(redirect_to)
                '''
                return render_json_response({'valid':True,'user':user}) 
            else:
                '''
                return redirect(reverse('userena_disabled',
                                        kwargs={'username': user.username}))
                '''
                
                
                data = {'valid': False}
                template = loader.get_template('authapi/signin_form.html')
                data['html'] = template.render(Context({'form':form}))
                return render_json_response(data)
    return render_json_response({'valid':False,'html':loader.get_template('authapi/signin_form.html').render(Context({'form':form}))})

@login_required
def friends(request,username,ftype):
    ctx = {}
    view_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated() and request.user.username == username:
        ctx['ftype']=ftype
        #ctx['timelines'] = view_user.timeline_set.exclude(status='del').order_by('-updated_on')
    else:
        ctx['ftype'] = ''
        #ctx['timelines'] = get_all_timlines().filter(created_by=view_user)
    return _friends(request, username, extra_context=ctx)
    
def test(request):
    print '==============================='
    pass
    

'''
def delete_follow(request):
    following_created = Following.objects.add_follower(request.user, other_user)
    pass
'''

def follow(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('userena_profile_list'))
    elif request.method == 'GET':
        user = get_object_or_404(User, username=request.GET.get('user'))
        ex_user=get_object_or_404(User,username=request.GET.get('ex_user'))
        if user and ex_user:
            user = get_object_or_404(User, username=user)
            ex_user=get_object_or_404(User,username=ex_user)
            result = Follow.objects.add_follower(follower=user,followee=ex_user)
            username = user.username
        else:
            raise Http404
        return HttpResponseRedirect(reverse('friend_list',kwargs={'username':username,'ftype':'following'}))
    else:
        raise Http404
    

def remove_follow(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('userena_profile_list'))
    elif request.method == 'GET':
        user = get_object_or_404(User, username=request.GET.get('user'))
        ex_user=get_object_or_404(User,username=request.GET.get('ex_user'))
        username=user.username
        if user and ex_user:
            result=Follow.objects.remove_follower(follower=user,followee=ex_user)
            #rel = Follow.objects.get(follower=user.id, followee=ex_user.id)
            #rel.delete()     
        else:
            raise Http404
        return HttpResponseRedirect(reverse('friend_list',kwargs={'username':username,'ftype':'following'}))
    else:
        raise Http404
        
    
            

def describe_email(request):
    return RSSFeed()

def describe_rss(request):
    return RSSFeed()

    
    