class Location(models.Model):
    notes = models.TextField(required = False)
    office = models.CharField(max_length = 2, choices = OFFICE_CHOICES, required =
      False)
    postal_address = models.TextField(required = False)
    room = models.TextField(required = False)
    coordinates = GPSCoordinate(required = False)

class TextEmailField(models.EmailField):
    entity = models.ForeignKey(Entity)
    def get_internal_type(self):
        return u'TextField'

class TextPhoneField(models.TextField):
    number = TextField()
    description = TextField()
    def __eq__(self, other):
        try:
            return self.remove_formatting() == other.remove_formatting()
        except:
            return False
    def remove_formatting(self):
        return re.sub(ur'\D', u'', str(self))

class TextURLField(models.URLField):
    def get_internal_type(self):
        return u'TextField'
