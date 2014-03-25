@login_required
def changelog(request):
    candidates = \
      directory.models.EditTrail.objects.filter(in_effect = True).order_by(
      u'change_set')    messages = []    for chunk in candidates:
        change = chunk
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
        message = change.username.title() + u' '
        if change.change_type == FOREIGN_KEY_RELATIONSHIP_CHANGED:
            message += u'changed ' + change.field_name + u' on ' + \ 
              model_name + u' from ' + \ 
              get_description(change.foreign_key_deleted) + u' to ' + \ 
              get_description(change.foreign_key_added) + u'.'
        elif change.change_type == INSTANCE_CREATED:
            message += u'created '
            if model_name.lower() in u'aeiou':
                message += u'n'
            message += u' ' + model_name + u'.'
        elif change.change_type == INSTANCE_DELETED:
            message += u'deleted ' + \ 
              model_name + u'.'
        elif change.change_type == MANY_TO_ONE_RELATIONSHIP_ADDED or \
          change.change_type == MANY_TO_MANY_RELATIONSHIP_ADDED:
            message += u'added a link from ' + model_name + u' to ' + \ 
              get_description(change.foreign_key_added) + u'.'
        elif change.change_type == MANY_TO_ONE_RELATIONSHIP_DELETED or \
          change.change_type == MANY_TO_MANY_RELATIONSHIP_DELETED:
            message += u'deleted a link from ' + model_name + u' from ' + \ 
              get_description(change.foreign_key_deleted) + u'.'
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
        else:
            message += change.change_type
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
