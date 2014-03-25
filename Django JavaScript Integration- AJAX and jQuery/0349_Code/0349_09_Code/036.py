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
