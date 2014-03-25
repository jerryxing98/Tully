def redirect(request, original_url):
    if original_url == u'create/Entity':
        return HttpResponsePermanentRedirect(u'/manage/Entity')
    elif original_url == u'create/Location':
        return HttpResponsePermanentRedirect(u'/manage/Location')
    else:
        return HttpResponseRedirect(u'/')
