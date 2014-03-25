@login_required
def profile(request, id):
    if id == "new":
        entity = directory.models.Entity()
        entity.save()
        id = entity.id
    else:
        entity = directory.models.Entity.objects.get(pk = int(id))
    emails = directory.models.EntityEmail.objects.filter(entity__exact =
      id).all()
