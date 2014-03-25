def image(request, id):
    return HttpResponse(open(directory.settings.DIRNAME +
      "/static/images/profile/" + id, "rb").read(),
      mimetype = directory.models.Entity.objects.filter(id = int(id))[0].image_mimetype)
