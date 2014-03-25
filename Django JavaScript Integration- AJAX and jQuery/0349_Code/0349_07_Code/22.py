    else:
        match = re.match(ur'^(.*?)_(.*)_(\d+)$', html_id)
        model = match.group(1)
        field = match.group(2)
        id = int(match.group(3))
        selected_model = get_model(u'directory', model)
        instance = selected_model.objects.get(pk = id)
        setattr(instance, field, value)
        instance.save()
        directory.functions.log_message(model + u'.' + field + u'(' + str(id) +
          u') changed by: ' + request.user.username + u' to: ' + value + u'\n')
        return HttpResponse(escape(value))
