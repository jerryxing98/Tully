class EntityPhoneField(TextPhoneField):
    entity = models.ForeignKey(Entity)
