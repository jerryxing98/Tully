    else:
        search = re.search(ur'(.*)_(\d+)', request.POST[u'id'])
        if search:
            getattr(directory.models, search.group(1)).objects.get(id =
              int(search.group(2))).delete()
