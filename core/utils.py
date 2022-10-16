import re

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
