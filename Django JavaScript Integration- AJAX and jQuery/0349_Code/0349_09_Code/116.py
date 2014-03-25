def homepage(request):
    id = u'null'
    try:
        query = request.REQUEST[u'query']
    except KeyError:
        query = u''
    try:
        id = request.REQUEST[u'id']
        if id:
            template = get_template(u'profile_internal.html')
            entity = directory.models.Entity.objects.filter(id = int(id))[0]
            if entity.gps:
                gps = entity.gps
            elif entity.location and entity.location.gps:
                gps = entity.location.gps
            else:
                gps = u''
            if gps:
                gps_url = \
                  u'http://maps.google.com/maps?f=q&source=s_q&hl=en&q=' \
                  + gps.replace(u' ', u'+') + "&iwloc=A&hl=en"
            else:
                gps_url = u''
            profile = template.render(Context(
                {
                u'entities': directory.models.Entity.objects.all(),
                u'entity': entity,
                u'first_stati': directory.models.Status.objects.filter(entity =
                  id).order_by(u'-datetime')[:directory.settings.INITIAL_STATI],
                u'gps': gps,
                u'gps_url': gps_url,
                u'id': int(id),
                u'emails': directory.models.Email.objects.all(),
                u'phones': directory.models.Phone.objects.all(),
                u'query': urllib.quote(query),
                u'second_stati': directory.models.Status.objects.filter(entity =
                  id).order_by(u'-datetime')[directory.settings.INITIAL_STATI:],
                u'tags': entity.tags.all().order_by(u'text'),
                u'urls': directory.models.URL.objects.all(),
                }))
    except KeyError:
        profile = u''
    try:
        if query:
            template = get_template(u'search_internal.html')
            tokens = re.split(ur'(?u)[^-\w]', query)
            while u'' in tokens:
                tokens.remove(u'')
            candidates = []
            for candidate in directory.models.Entity.objects.all():
                candidates.append([candidate, 0])
            for token in tokens:
                new_candidates = []
                for candidate in candidates:
                    if directory.functions.score(candidate[0], token) > 0:
                        candidate[1] += directory.functions.score(candidate[0], token)
                        new_candidates.append(candidate)
                candidates = new_candidates
                candidates.sort(lambda a, b: -cmp(a[1], b[1]))
                export = []
                for candidate in candidates:
                    if candidate[0].image_mimetype:
                        image = True
                    else:
                        image = False
                    export.append(
                        {
                        u'department': name,
                        u'description': candidate[0].description,
                        u'id': candidate[0].id,
                        u'image': image,
                        u'name': candidate[0].name,
                        u'title': candidate[0].title,
                        })
                first_portion = export[:directory.settings.INITIAL_RESULTS]
                second_portion = export[directory.settings.INITIAL_RESULTS:]
                                template = get_template(u'search_internal.html')
                search_results = template.render(Context(
                    {
                    u'first_portion': first_portion,
                    u'query': query,
                    u'second_portion': second_portion,
                    }))
        else:
            search_results = u''
    except KeyError:
        search_results = u''
    return render_to_response(u'search.html', Context(
        {
        u'profile': profile,
        u'query': urllib.quote(query),
        u'search_results': search_results,
        u'settings': directory.settings,
        }))
