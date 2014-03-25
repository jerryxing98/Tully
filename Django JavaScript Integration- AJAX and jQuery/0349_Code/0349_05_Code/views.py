#!/usr/bin/python   

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from directory.functions import ajax_login_required
        
import directory.models 
import json
import re

RESULTS_PER_PAGE = 10

def ajax_login_request(request):
    try:
        request.POST[u'login']
        dictionary = request.POST
    except:
        dictionary = request.GET
    user = authenticate(username = dictionary[u'login'], password = dictionary[u'password'])    
    if user and user.is_active:
        login(request, user)
        result = True
    else:
        result = False
    response = HttpResponse(json.dumps(result), mimetype = u'application/json')
    return response

@ajax_login_required
def search(request):
    try:
        query = request.POST[u'query']
        dictionary = request.POST
    except:
        query = request.GET[u'query']
        dictionary = request.GET
    split_query = re.split(ur'(?u)\W', query)
    while u'' in split_query:
        split_query.remove(u'')
    results = []
    for word in split_query:
        for entity in directory.models.Entity.objects.filter(name__icontains = word):
            if re.match(ur'(?ui)\b' + word + ur'\b', entity.name):
                entry = {u'id': entity.id, u'name': entity.name, u'description': entity.description}
            if not entry in results:
                results.append(entry)
    for entry in results:
        score = 0
        for word in split_query:
            if re.match(ur'(?ui)\b' + word + ur'\b', entry[u'name']):
                score += 1
        entry[u'score'] = score
    def compare(a, b):
        if cmp(a[u'score'], b[u'score']) == 0:
            return cmp(a[u'name'], b[u'name'])
        else:
            return -cmp(a[u'score'], b[u'score'])
    results.sort(compare)
    try: 
        start = int(dictionary[u'start'])
    except:
        start = 0
    try:
        results_per_page = int(dictionary[u'results_per_page'])
    except: 
        results_per_page = RESULTS_PER_PAGE
    returned_results = results[start:start + results_per_page]
    response = HttpResponse(json.dumps([returned_results, len(results)]),
      mimetype = u'application/json')
    return response

def homepage(request):
    return render_to_response(u'search.html')
