@ajax_login_required
def saveimage(request, string_id):
    id = int(string_id)
    entity = directory.models.Entity.objects.filter(id = id)[0]
    file = request.FILES.values()[0]
    extension = file.name.lower().split(".")[-1]
    if extension == u'jpg':
        entity.image_mimetype = u'image/jpeg'
    elif extension == u'swf':
        entity.image_mimetype = u'application/x-shockwave-flash'
    else:
        entity.image_mimetype = u'image/' + extension
    entity.save()
    save_file = open(directory.settings.DIRNAME + u'/static/images/profile/' +
      string_id, u'wb')
    for chunk in file.chunks():
        save_file.write(chunk)
    directory.functions.log_message(u'Image for entity ' + string_id +
      u' changed by ' + request.user.username +u'".')
    result = u'''<img class="profile" src="/profile/images/%d">''' % id
    return HttpResponse(result)
