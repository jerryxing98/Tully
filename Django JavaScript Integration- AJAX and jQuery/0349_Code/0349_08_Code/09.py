def modelform_Entity(request, id):
    if request.method == u'POST':
        form = directory.models.EntityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            form = directory.models.EntityForm(instance =
              directory.models.Entity.objects.get(pk = int(id)))
        except:
            form = directory.models.EntityForm()
    variables = RequestContext(request,
        {
        u'form': form,
        u'title': u'Entity',
        })
    return render_to_response(u'modelform.html', variables)

def modelform_Location(request, id):
    if request.method == u'POST':
        form = directory.models.LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            form = directory.models.LocationForm(instance =
              directory.models.Location.objects.get(pk = int(id)))
        except:
            form = directory.models.LocationForm()
    variables = RequestContext(request,
        {
        u'form': form,
        u'title': u'Location',
        })
    return render_to_response(u'modelform.html', variables)
