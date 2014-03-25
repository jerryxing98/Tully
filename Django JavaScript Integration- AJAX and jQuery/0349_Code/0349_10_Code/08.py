        change_set = register_edit(INSTANCE_CREATED, status, session, username,
          request.META[u'REMOTE_ADDR'])
        register_edit(TEXT_CHANGED, status, session, username,
          request.META[u'REMOTE_ADDR'], field_name = u'text', change_set =
          change_set, text_after = value)
        return HttpResponse(u'<!--# ' + unicode(change_set) + u' #-->')
    match = re.match(ur'Email_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        email = directory.models.Email(email = value, entity =
          directory.models.Entity.objects.get(id = model))
        email.save()
        directory.functions.log_message(u'Email for Entity ' +
          str(model) + u' added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        change_set = register_edit(INSTANCE_CREATED, email, session, username,
          request.META[u'REMOTE_ADDR'])
        register_edit(TEXT_CHANGED, email, session, username,
          request.META[u'REMOTE_ADDR'], field_name = u'email', text_after =
          value)
