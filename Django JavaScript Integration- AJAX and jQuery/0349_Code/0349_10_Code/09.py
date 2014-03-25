        return HttpResponse(u'<!--# ' + unicode(change_set) + u' #-->')
    match = re.match(ur'Entity_tag_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
        entity = directory.models.Entity.objects.get(id = model)
        names = value.lower().split(" ")
        response_text = ""
        change_set = None
        for name in names:
            if name:
                if not directory.models.Tag.objects.filter(text = name, entity
                  = entity, is_invisible = False):
                    tag = directory.models.Tag(text = name, entity = entity)
                    tag.save()
                    response_text += "<span class='tag'>" + name + \
                      "</span> &nbsp; "
                    if change_set != None:
                        register_edit(MANY_TO_ONE_RELATIONSHIP_ADDED, tag,
                          session, username, request.META[u'REMOTE_ADDR'],
                          change_set = change_set, field_name = u'entity',
                          foreign_key_added = entity)
                    else:
                        change_set = \
                          register_edit(MANY_TO_ONE_RELATIONSHIP_ADDED,
                          tag, session, username, request.META[u'REMOTE_ADDR'],
                          field_name = u'entity', foreign_key_added = entity)
        entity.save()
        directory.functions.log_message(u'Tags for Entity ' +
          str(match.group(1)) + u' added by: ' + request.user.username +
          u', value: ' + value + u'\n')
        return HttpResponse(u'<!--# ' + unicode(change_set) + u' #-->')
    match = re.match(ur'Tag_new_(\d+)', html_id)
