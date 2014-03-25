    if request.POST[u'id'].lower().startswith(u'tag_'):
        search = re.search(ur'[Tt]ag_(\d+)_(\d+)', request.POST[u'id'])
        if search:
            entity = directory.models.Entity.objects.get(id =
              int(search.group(1)))
            entity.tags.remove(directory.models.Tag.objects.get(id =
              int(search.group(2))))
            entity.save()
