#!/usr/bin/env python
#coding=utf-8
'''
Created on 2014-1-20

@author: Jerryminds
'''

import os
import os.path
import collections
from django.http import HttpResponse
from django.template import Context, Template
from django.utils.functional import Promise
from django.utils.encoding import force_unicode


root_path = os.path.dirname(__file__)

def get_path(s):
    if isinstance(s, str):
        return os.path.join(root_path, s)
    elif isinstance(s, collections.Iterable):
        return os.path.join(root_path, os.sep.join(s)) 
        



try:
    from simplejson import JSONEncoder
except ImportError:
    try:
        from json import JSONEncoder
    except ImportError:
        from django.utils.simplejson import JSONEncoder

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

def render_json_response(data):
    json_serializer = LazyEncoder()
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')

def render_form(form):
    data = {'valid': True}
    data['html'] = render_string("{{ form }}", {'form': form})
    return render_json_response(data)

def render_string(tmpl, ctx):
    return Template(tmpl).render(Context(ctx))
