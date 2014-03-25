from django.db import models
from django.core.exceptions import ValidationError
import re

def gps_validator(value):
    # Create a normalized working copy of the value.
    working_copy = value
    working_copy = working_copy.replace(u'\n', u',')
    working_copy = working_copy.replace(u'\r', u',')
    working_copy = re.sub(ur',*$', '', working_copy)
    working_copy = re.sub(ur',+', u',', working_copy)
    if not u',' in working_copy and not \
      re.match(ur'.* .* .*', working_copy):
        working_copy = working_copy.replace(u' ', u',')
    working_copy = re.sub(u'[\00B0\2018\2019\201C\201D\'"]', ' ', working_copy)
    working_copy = working_copy.replace(u',', u', ')
    working_copy = re.sub(ur'\s+', u' ', working_copy)
    working_copy = working_copy.strip()
    working_copy = working_copy.upper()
    # Test the normalized working copy against regular expressions for different kinds of GPS format.
    if re.match(ur'[-NS]? ?\d{1,3} [0-5]\d [0-5]\d(\.\d+)[NS]?, [-EW]? ?\d{1,3} [0-5]\d [0-5]\d(\.\d+)[EW]?', working_copy):
        return working_copy
    elif re.match(ur'[-NS]? ?\d{1,3} [0-5]\d(\.\d+)[NS]?, [-EW]? ?\d{1,3} [0-5]\d(\.\d+)[EW]?', working_copy):
        return working_copy
    elif re.match(ur'[-NS]? ?\d{1,3}(\.\d+)[NS]?, [-EW]? ?\d{1,3}(\.\d+)[EW]?', working_copy):
        return working_copy
    else:
        raise ValidationError(u'We could not recognize this as a valid GPS coordinate.')

class GPSField(models.TextField):
    default_error_messages = {
        u'invalid': u'We could not recognize this as a valid GPS coordinate.',
      }
    default_validators = [gps_validator]
