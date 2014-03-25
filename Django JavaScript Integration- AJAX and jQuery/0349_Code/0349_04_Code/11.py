
class TextStatus(models.Model):
    datetime = models.DateTimeField(default=datetime.now)
    entity = models.ForeignKey(Entity)
    text = models.TextField()
