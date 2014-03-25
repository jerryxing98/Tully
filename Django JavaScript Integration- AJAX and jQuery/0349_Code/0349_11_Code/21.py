class Entity(models.Model):
    active = models.BooleanField(blank = True)
    department = models.ForeignKey(u'self', blank = True, null =
      True, related_name = u'member')
    description = models.TextField(blank = True)
    gps = GPSField()
    image_mimetype = models.TextField(blank = True, null = True)
    is_invisible = models.BooleanField(default = False)
    location = models.ForeignKey(u'self', blank = True, null = True,
      related_name = u'occupant')
    name = models.TextField(blank = True, default = u'(Insert name here)')
    observes_daylight_saving_time = models.BooleanField(blank = True, default
      = True)
    other_contact = models.TextField(blank = True)
    postal_address = models.TextField(blank = True)
    publish_externally = models.BooleanField(blank = True)
    reports_to = models.ForeignKey(u'self', blank = True, null = True,
      related_name = u'subordinate')
    start_date = models.DateField(blank = True, null = True)
    time_zone = models.CharField(max_length = 5, null = True, choices =
      TIME_ZONE_CHOICES)
    title = models.TextField(blank = True)
    class Meta:
        permissions = (
          ("view_changelog", "View the editing changelog"),
          )
