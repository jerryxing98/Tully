    return render_to_response(u'profile_internal.html',
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
        u'second_stati': directory.models.Status.objects.filter(entity =
          id).order_by(u'-datetime')[directory.settings.INITIAL_STATI:],
        u'tags': entity.tags.all().order_by(u'text'),
        u'urls': directory.models.URL.objects.all(),
        })
