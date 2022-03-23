import re

from django.http            import JsonResponse
from django.core.exceptions import ValidationError

EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$'

def validate_email(value):
    if not re.match(EMAIL_REGEX, value):
        raise ValidationError('INVALID_EMAIL')

def validate_password(value):
    if not re.match(PASSWORD_REGEX, value):
        raise ValidationError('INVALID_PASSWORD')

##### raise 대신 return 하게 되면 JsonResponse 객체를 반환할 뿐 코드는 계속해서 실행됨 #####
def test_validation(value):
    if not re.match(EMAIL_REGEX, value):
        return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)