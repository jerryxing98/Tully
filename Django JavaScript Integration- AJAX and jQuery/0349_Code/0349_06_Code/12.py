class Location(models.Model):
    identifier = models.TextField(blank = True)
    description = models.TextField(blank = True)
    office = models.CharField(max_length = 2, choices = OFFICE_CHOICES, blank =
      True)
    postal_address = models.TextField(blank = True)
    room = models.TextField(blank = True)
    coordinates = GPSField(blank = True)
