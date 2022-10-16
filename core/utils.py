import re
import jwt

from django.http        import JsonResponse
from django.conf        import settings

from users.models       import User
from companies.models   import Company

def check_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(REGEX_EMAIL, email):
        raise ValueError("invalid email_format")

def duplicate_check_username(name):
    if Company.objects.filter(name = name).exists():
        raise ValueError("duplicate_company_name")

def duplicate_check_email(email):
    if User.objects.filter(email = email).exists():
        raise ValueError("duplicate_email")

def login_user_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user         = User.objects.get(id = payload['id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'invalid_token'}, status= 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'invalid_user'}, status=400)

    return wrapper

def login_company_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            company      = Company.objects.get(id = payload['id'])
            request.user = company

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'invalid_token'}, status= 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'invalid_company'}, status=400)

    return wrapper