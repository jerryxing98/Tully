#!/usr/bin/python/

import json
import time
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    return render_to_response(u'clock_skew.html')

def timestamp(request): 
    return HttpResponse(json.dumps({u'time': 1000 * time.time()}), mimetype=u'application/json')
