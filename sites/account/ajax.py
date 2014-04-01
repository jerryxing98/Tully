# -*- coding: UTF-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from bookmark.views import recommend
from django.template import RequestContext, loader
from django.shortcuts import render
from bookmark.forms import BKCommentForm
from django.contrib.auth import login,authenticate,logout
from account.forms import BsAuthenticationForm
from userena.forms import SignupForm,SignupFormOnlyEmail,AuthenticationForm,ChangeEmailForm,EditProfileForm
from dajaxice.utils import deserialize_form
from  django.shortcuts import render_to_response


@dajaxice_register(method='GET',name='account.ajax_login_get')
@dajaxice_register(method='POST',name='account.ajax_login_post')
def ajax_login(request,form):
    t=loader.get_template('authapi/signin_form.html')
    if request.method =='POST':
        #dajax = Dajax()
        form = BsAuthenticationForm(deserialize_form(form))
        if form.is_valid():
            #dajax.dajax.remove_css_class('#signin_form input', 'error')
            identification, password, remember_me = (form.cleaned_data['identification'],
                                                     form.cleaned_data['password'],
                                                     form.cleaned_data['remember_me'])
            user = authenticate(identification=identification,
                                password=password)
            if user and user.is_active:
                login(request, user)
                variables=RequestContext(request)
                html=render_to_response('authapi/nav_signin.html',variables)
                result = {'status':'Success','message':html.content}
                return simplejson.dumps(result)
            else:
                return simplejson.dumps({'status':'Fail','error':'用户未激活'})
        else:
            #dajax.remove_css_class('#signin_form input', 'error')
            #for error in form.errors:
            #    dajax.add_css_class('#id_%s' % error, 'error')
            html = render(request, 'authapi/signin_form.html', {'form':form})
            return simplejson.dumps({'status':'Error','message':html.content})
        return dajax.json()
    if request.method == 'GET':
        auth_form = BsAuthenticationForm()
        tip= request.session['Tip']
        if tip:
            auth_form.errors['Tip']=tip
        html = render(request, 'authapi/signin_form.html', {'form':auth_form})
        return simplejson.dumps({'message':html.content})


@dajaxice_register
def ajax_logout(request):
    if request.user.is_authenticated():
        logout(request)
    variables=RequestContext(request)
    html=render_to_response('authapi/nav_signin.html',variables)
    result = {'status':'Success','message':html.content}
    return simplejson.dumps(result)
    