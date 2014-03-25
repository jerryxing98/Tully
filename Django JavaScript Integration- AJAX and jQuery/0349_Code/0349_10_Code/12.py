    change_set = register_edit(IMAGE_CHANGED, entity, session,
      request.user.username, request.META[u'REMOTE_ADDR'], text_before =
      original_mimetype, text_after = entity.image_mimetype)
    result = u'''<img class="profile" src="/profile/images/%d">''' % id + \
      u'<!--# ' + change_set + u' #-->'
    return HttpResponse(result)
