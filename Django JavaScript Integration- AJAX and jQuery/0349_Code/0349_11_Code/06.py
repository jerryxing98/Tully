def ajax_download_model(request, model):
    if directory.settings.SHOULD_DOWNLOAD_DIRECTORY:
        json_serializer = serializers.get_serializer(u'json')()
        response = HttpResponse(mimetype = u'application/json')
        if model == u'Entity':
            json_serializer.serialize(getattr(directory.models,
              model).objects.filter(is_invisible = False).order_by(u'name'),
              ensure_ascii = False, stream = response)
        else:
            json_serializer.serialize(getattr(directory.models,
              model).objects.filter(is_invisible = False), ensure_ascii = False,
              stream = response)
        return response
    else:
        return HttpResponse(u'This feature has been turned off.')
