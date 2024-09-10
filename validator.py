import re
from django.core.exceptions import ValidationError

def validate_kenya_phone_number(value):
    if not value.startswith('+254'):
        raise ValidationError('Phone number must start with +254')
    if not re.match(r'^\+254\d{9}$', value):
        raise ValidationError('Phone number must be a valid Kenyan number starting with +254 followed by 9 digits')
