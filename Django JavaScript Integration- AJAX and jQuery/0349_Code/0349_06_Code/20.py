@login_required
def profile(request, id):
    entity = directory.models.Entity.objects.get(pk = id)
    emails = directory.models.EntityEmail.objects.filter(entity__exact =
      id).all()
    return HttpResponse(get_template(u'profile.html').render(Context(
      {u'entity': entity, u'emails': emails})))
