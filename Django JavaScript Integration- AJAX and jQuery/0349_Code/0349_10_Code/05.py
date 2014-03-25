@ajax_login_required
def ajax_delete(request):
    session = request.session.session_key
    username = request.user.username
    change_set = None
    search = re.search(ur'(.*)_(\d+)', request.POST[u'id'])
    if search:
        model = getattr(directory.models, search.group(1)).objects.get(id =
          int(search.group(2)))
        change_set = register_edit(INSTANCE_DELETED, model, session,
          username, request.META[u'REMOTE_ADDR'])
        model.is_invisible = True
        model.save()
    directory.functions.log_message(u'Deleted: ' + request.POST[u'id'] +
      u' by ' + request.user.username + u'.')
    if change_set == None:
        return HttpResponse(u'')
    else:
        response = u'<!--# ' + str(change_set) + u' #-->'
        return HttpResponse(response)
