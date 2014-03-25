from django.db import models

class CreditCardNumber(models.TextField):
    def clean(self):
        return re.sub(r'\D', '', str(self))
