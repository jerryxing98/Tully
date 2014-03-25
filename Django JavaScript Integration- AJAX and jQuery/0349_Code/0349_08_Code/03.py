@login_required
def modelform_Entity(request):
    if request.method == u'POST':
        form = directory.models.EntityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = directory.models.EntityForm()
    variables = RequestContext(request,
        {
        u'form': form,
        u'title': u'Entity',
        })
    return render_to_response(u'modelform.html', variables)

@login_required
def modelform_Location(request):
    if request.method == u'POST':
        form = directory.models.LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = directory.models.LocationForm()
    variables = RequestContext(request,
        {
        u'form': form,
        u'title': u'Location',
        }) 
    return render_to_response(u'modelform.html', variables)
