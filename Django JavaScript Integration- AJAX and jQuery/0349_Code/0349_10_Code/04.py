def register_edit(change_type, instance, session, username, ip, change_set =
  None, content_type = None, field_name = None, foreign_key_added = None,
  foreign_key_deleted = None, text_before = None, text_after = None):
    edit = directory.models.EditTrail()
    edit.object_id = instance.id
    if change_set:
        edit.change_set = change_set
    else:
        increment = directory.models.Increment()
        increment.save()
        edit.change_set = increment.id
    edit.change_type = change_type
    edit.field_name = field_name
    edit.in_effect = True
    edit.instance = instance
    edit.ip = ip
    edit.timestamp = datetime.datetime.now()
    edit.username = username
    if change_type == directory.models.TEXT_CHANGED:
        edit.text_before = text_before
        edit.text_after = text_after
    elif change_type in (directory.models.FOREIGN_KEY_RELATIONSHIP_CHANGED,
      directory.models.MANY_TO_MANY_RELATIONSHIP_ADDED,
      directory.models.MANY_TO_MANY_RELATIONSHIP_DELETED,
      directory.models.MANY_TO_ONE_RELATIONSHIP_ADDED,
      directory.models.MANY_TO_ONE_RELATIONSHIP_DELETED):
        if foreign_key_added:
            edit.foreign_key_added = foreign_key_added
        if foreign_key_deleted:
            edit.foreign_key_deleted = foreign_key_deleted
    edit.save()
    return edit.change_set
