# -*- coding: UTF-8 -*-
from dajaxice.decorators import dajaxice_register
from bookmark.views import recommend
from django.template import RequestContext, loader
from bookmark.forms import BKCommentForm
from account.ajax import ajax_login
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404
from dajaxice.utils import deserialize_form
from  django.shortcuts import render_to_response
from ajax_validation.views import validate_form
from account.forms import BsAuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from favorite.models import Favorite


@dajaxice_register(method='POST',name='favorite.add_or_remove')
def add_or_remove(request,target_model,pk):
    if request.method=="POST":
        user = request.user
        if not user.is_authenticated():
            form = ""
            request.session['Tip']=u'   you are anonymous,Please login!'
            request.method="GET"
            return ajax_login(request,form)

        
        target_model = get_model(*target_model.split('.') or None)
        target_content_type = ContentType.objects.get_for_model(target_model)
        target = target_content_type.get_object_for_this_type(pk=pk)
        # delete it if it's already a faorite
        if user.favorite_set.filter(target_content_type=target_content_type,
                                 target_object_id=pk):
            user.favorite_set.get(target_content_type=target_content_type,
                                     target_object_id=pk).delete()
            status = 'deleted'

        # otherwise, create it
        else:
            user.favorite_set.create(target_content_type=target_content_type,
                                     target_object_id=pk)
            status = 'added'
        
        
        response = {'status': status,'message':[target.pk,Favorite.objects.filter(target_content_type=target_content_type,
                                                         target_object_id=pk).count()]}
        return simplejson.dumps(response)

