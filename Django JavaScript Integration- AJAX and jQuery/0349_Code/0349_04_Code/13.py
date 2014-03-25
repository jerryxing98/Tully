#!/usr/bin/python

from django.core import serializers

RESULTS_PER_PAGE = 10

def search(request):
    query = request.POST[u'query']
    split_query = re.split(ur'(?u)\W', query)
    while u'' in split_query:
        split_query.remove(u'')
