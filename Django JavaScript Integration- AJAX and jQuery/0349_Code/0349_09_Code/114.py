match = re.match(ur'Status_new_(\d+)', html_id)
    if match:
        status = directory.models.Status(entity =
          directory.models.Entity.objects.get(id = int(match.group(1))),
          text = value)
        status.save()
        directory.functions.log_message(u'Status for Entity ' +
          str(match.group(1)) + u' added by: ' + request.user.username +
          u', value: ' + value + u'\n')
        return HttpResponse(u'')
    match = re.match(ur'Email_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        email = directory.models.Email(email = value, entity =
          directory.models.Entity.objects.get(id = model))
        email.save()
        directory.functions.log_message(u'Email for Entity ' +
          str(model) + u' added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        return HttpResponse(u'')
    match = re.match(ur'Entity_tag_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        entity = directory.models.Entity.objects.get(id = model)
        names = value.lower().split(" ")
        response_text = ""
        for name in names:
            if name:
                try:
                    tag = directory.models.Tag.objects.filter(text__exact = name)[0]
                except (AttributeError, IndexError):
                    tag = directory.models.Tag(text = name)
                    tag.save()
                if not tag in entity.tags.all():
                    response_text += "<span class='tag'>" + name + \
                      "</span> &nbsp; "
                    entity.tags.add(tag)
        entity.save()
        directory.functions.log_message(u'Tags for Entity ' +
          str(match.group(1)) + u' added by: ' + request.user.username +
          u', value: ' + value + u'\n')
        return HttpResponse(u'')
    match = re.match(ur'URL_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        url = directory.models.URL(url = value, entity =
          directory.models.Entity.objects.get(id = model))
        url.save()
        directory.functions.log_message(u'URL for Entity ' +
          str(model) + u') added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        return HttpResponse(u'')
    match = re.match(ur'Phone_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        phone = directory.models.Phone(number = value, entity =
          directory.models.Entity.objects.get(id = model))
        phone.save()
        directory.functions.log_message(u'Phone for Entity ' +
          str(model) + u') added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        return HttpResponse(u'')
    elif html_id.startswith(u'Entity_department_'):
        entity_id = int(html_id[len(u'Entity_department_'):])
        entity = directory.models.Entity.objects.get(id = entity_id)
        department_id = int(value[len(u'department.'):])
        if department_id == -1:
            entity.department = None
        else:
            entity.department = directory.models.Entity.objects.get(id =
              department_id)
        directory.functions.log_message(u'Department for Entity ' +
          str(entity_id) + u') set by: ' + request.user.username +
          u', value: ' + value + u'\n')
                entity.save()
        return HttpResponse(value)
    elif html_id.startswith(u'Entity_location_'):
        entity_id = int(html_id[len(u'Entity_location_'):])
        entity = directory.models.Entity.objects.get(id = entity_id)
        location_id = int(value[len(u'location.'):])
        if location_id == -1:
            entity.location = None
        else:
            entity.location = directory.models.Entity.objects.get(id =
              location_id)
        directory.functions.log_message(u'Location for Entity ' +
          str(entity_id) + u') set by: ' + request.user.username +
          u', value: ' + value + u'\n')
        entity.save()
        return HttpResponse(value)
    elif html_id.startswith(u'Entity_reports_to_'):
        entity_id = int(html_id[len(u'Entity_reports_to_'):])
        entity = directory.models.Entity.objects.get(id = entity_id)
        reports_to_id = int(value[len(u'reports_to.'):])
        entity = directory.models.Entity.objects.get(id = entity_id)
        if reports_to_id == -1:
            entity.reports_to = None
        else:
            entity.reports_to = directory.models.Entity.objects.get(id =
              reports_to_id)
        directory.functions.log_message(u'reports_to for Entity ' +
          str(entity_id) + u') set by: ' + request.user.username +
          u', value: ' + value + u'\n')
        entity.save()
        return HttpResponse(value)
    else:
        match = re.match(ur'^(.*?)_(.*)_(\d+)$', html_id)
        model = match.group(1)
        field = match.group(2)
        id = int(match.group(3))
        selected_model = get_model(u'directory', model)
        instance = selected_model.objects.get(id = id)
        setattr(instance, field, value)
        instance.save()
        directory.functions.log_message(model + u'.' + field + "(" + str(id) +
          u') changed by: ' + request.user.username + u' to: ' + value + u'\n')
        return HttpResponse(escape(value))
