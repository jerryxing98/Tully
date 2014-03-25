    results = []
    for word in split_query:
        for entity in Entity.objects.filter(name__icontains = word):
            if re.match(ur'(?ui)\b' + word + ur'\b'):
                entry = {u'id': entity.id, u'name': entity.name, u'description': entity.description}
            if not entry in results:
                results.append(entry)
