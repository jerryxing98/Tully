    reports_to = models.ForeignKey(Entity, required = False)
    start_date = models.DateField(required = False)

# Tagging is intended at least initially to locate areas of expertise
tagging.register(Entity)
