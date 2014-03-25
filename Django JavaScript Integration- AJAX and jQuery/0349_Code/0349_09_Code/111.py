def ajax_download_model(request, model):
    if directory.settings.SHOULD_DOWNLOAD_DIRECTORY:
        json_serializer = serializers.get_serializer(u'json')()
        response = HttpResponse(mimetype = u'application/json')
        json_serializer.serialize(getattr(directory.models,
          model).objects.all(), ensure_ascii = False, stream = response)
        return response
    else:
        return HttpResponse(u'This feature has been turned off.')
