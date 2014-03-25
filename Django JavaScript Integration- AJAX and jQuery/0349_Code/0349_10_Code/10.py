@ajax_login_required
def saveimage(request, string_id):
    id = int(string_id)
    entity = directory.models.Entity.objects.filter(id = id)[0]
    original_mimetype = entity.image_mimetype
    file = request.FILES.values()[0]
    extension = file.name.lower().split(".")[-1]
    if extension == u'jpg':
        entity.image_mimetype = u'image/jpeg'
    elif extension == u'swf':
        entity.image_mimetype = u'application/x-shockwave-flash'
    else:
        entity.image_mimetype = u'image/' + extension
    entity.save()
