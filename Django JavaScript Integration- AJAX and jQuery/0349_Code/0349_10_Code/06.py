@ajax_login_required
def new_Entity(request):
    entity = directory.models.Entity()
    entity.save()
    json_serializer = serializers.get_serializer(u'json')()
    response = HttpResponse(mimetype = u'application/json')
    register_edit(INSTANCE_CREATED, entity, request.session.session_key,        
      request.user.username, request.META[u'REMOTE_ADDR'])
    json_serializer.serialize([entity], ensure_ascii = False, stream = response)
    return response
