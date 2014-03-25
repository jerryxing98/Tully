import django.forms
import re

EXTENSION_LENGTH = 5

def is_extension(number):
    if len(str(number)) > EXTENSION_LENGTH:
        raise forms.ValidationError(u'This extension is too long.')
    #elif len(str(number)) < EXTENSION_LENGTH:
        #raise forms.ValidationError(u'This extension is too short.')
    else:
        return text
    
class ExtensionField(PositiveIntegerField):
    default_error_messages = {
      u'invalid': u'Enter a valid extension.',
      }
    default_validators = [is_extension]
