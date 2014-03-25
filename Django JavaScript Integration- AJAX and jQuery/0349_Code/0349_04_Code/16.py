    try: 
        start = int(request.POST[u'start'])
    except:
        start = 0
    try:
        results_per_page = int(request.POST[u'results_per_page'])
    except:
        results_per_page = RESULTS_PER_PAGE
    returned_results = results[start:start + results_per_page]
    json_serializer = serializers.get_serialized(u'json')()
    response = HttpResponse()
    response[u'Content-type'] = u'text/json'
    json_serializer.serialize([returned_results, len(results)], ensure_ascii = False, stream = response)
    return response
