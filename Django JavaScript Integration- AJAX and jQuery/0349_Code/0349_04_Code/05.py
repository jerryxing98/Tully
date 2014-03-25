# This class is basically the "Person" class; however, it is called "Entity"
# to emphasize that it is intended to accommodate people, offices,
# organizational units, and possibly other areas.
class Entity(models.Model):
    active = models.BooleanField(required = False)
    department = models.ForeignKey(Entity, required = False)
