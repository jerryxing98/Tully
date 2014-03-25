from django.db import models

class TextEmailField(models.EmailField):
    def get_internal_type(self):
        return 'TextField'
