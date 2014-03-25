@login_required
def changelog(request):
    candidates = \
      directory.models.EditTrail.objects.filter(in_effect = True).order_by(
      u'change_set')
    messages = []
    for candidate in candidates:
        message = None
        change = candidate
        id = change.change_set
        model_name = unicode(type(change.instance))[7:-2]
        description = ''
        def get_description(instance):
            description = u''
            if not instance:
                return u''
            instance_model_name = unicode(type(instance))[7:-2].split(u'.')[-1]
            if hasattr(instance, u'name') and instance.name:
                description += u' ' + instance.name + u', '
            description += u'a'
            if instance_model_name and instance_model_name[0].lower() in \
              u'aeiou':
                description += u'n'
            description += u' ' + instance_model_name
            return description
        model_name = get_description(change.instance)
        timestamp = change.format_timestamp()
        if change.change_type == INSTANCE_DELETED:
            message = change.username.title() + u' '
            message += u'deleted ' + \
              model_name + u'.'
        elif change.change_type == TEXT_CHANGED:
            message = change.username.title() + u' changed the ' + \
              change.field_name + u' on ' + description + \
              u' from "'
            if change.text_before:
                message += change.text_before
            message += u'" to "'
            if change.text_after:
                message += change.text_after
            message += u'".'
        if message:
            messages.append(
                {
                u'change_set': id,
                u'message': message,
                u'timestamp': timestamp,
                })
    return render_to_response(u'changelog.html',
      {
      u'messages': messages,
      u'settings': directory.settings,
      })
