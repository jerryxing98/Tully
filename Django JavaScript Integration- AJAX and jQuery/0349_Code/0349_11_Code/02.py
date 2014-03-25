    return render_to_response(u'profile_internal.html',
        {
        u'entities': directory.models.Entity.objects.filter(is_invisible =
          False).order_by(u'name'),
        u'entity': entity,
        u'first_stati': directory.models.Status.objects.filter(entity =
          id).order_by(u'-datetime')[:directory.settings.INITIAL_STATI],
        u'gps': gps,
        u'gps_url': gps_url,
        u'id': int(id),
        u'emails': directory.models.Email.objects.filter(entity = entity,
          is_invisible = False),
        u'phones': directory.models.Phone.objects.filter(entity = entity,
          is_invisible = False),
        u'second_stati': directory.models.Status.objects.filter(entity =
          id).order_by(u'-datetime')[directory.settings.INITIAL_STATI:],
        u'tags': directory.models.Tag.objects.filter(entity = entity,
          is_invisible = False).order_by(u'text'),
        u'time_zones': directory.models.TIME_ZONE_CHOICES,
        u'urls': directory.models.URL.objects.filter(entity = entity,
          is_invisible = False),
        })
