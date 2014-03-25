@login_required
def profile(request, id):
    entity = directory.models.Entity.objects.get(pk = id)
    emails = directory.models.EntityEmail.objects.filter(entity__exact =
      id).all()
    all_entities = directory.models.Entity.objects.all()
    all_locations = directory.models.Location.objects.all()
    return HttpResponse(get_template(u'profile.html').render(Context(
      {
      u'entity': entity,
      u'emails': emails,
      u'departments': all_entities,
      u'reports_to_candidates': all_entities,
      u'locations': all_locations,
      })))
