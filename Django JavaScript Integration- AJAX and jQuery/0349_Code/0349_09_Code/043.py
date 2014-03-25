def ajax_search(request):
    try:
        query = request.POST[u'query']
    except KeyError:
        try:
            query = request.GET[u'query']
        except KeyError:
            return HttpResponse(u'')
    tokens = re.split(ur'(?u)[^-\w]', query)
    while u'' in tokens:
        tokens.remove(u'')
