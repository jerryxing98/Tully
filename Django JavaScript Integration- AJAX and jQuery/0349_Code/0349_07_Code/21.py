    elif html_id.startswith(u'Entity_department_'):
        entity_id = int(html_id[len(u'Entity_department_'):])
        department_id = int(value[len(u'department.'):])
        entity = directory.models.Entity.objects.get(pk = entity_id)
        if department_id == -1: 
            entity.department = None
        else:
            entity.department = directory.models.Entity.objects.get(pk =
              department_id)
        entity.save()
        return HttpResponse(value)
    elif html_id.startswith(u'Entity_location_'):
        entity_id = int(html_id[len(u'Entity_location_'):])
        location_id = int(value[len(u'location.'):])
        if location_id == -1: 
            entity.location = None
        else:
            entity.location = directory.models.Location.objects.get(pk ==
              location_id)
        entity.save()
        return HttpResponse(value)
    elif html_id.startswith(u'Entity_reports_to_'):
        entity_id = int(html_id[len(u'Entity_reports_to'):])
        reports_to_id = int(value[len(u'reports_to.'):]) 
        entity = directory.models.Entity.object.get(pk = entity_id)
        if reports_to_id == -1: 
            entity.reports_to = None
        else:
            entity.reports_to = directory.models.Entity.objects.get(pk ==
              reports_to_id)
        entity.save()
        return HttpResponse(value)
