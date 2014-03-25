from django.db import models

class PhoneNumber(models.TextField):
    def clean(self):
        return re.sub(r'\W', '', str(self))
