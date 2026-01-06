from django.contrib.auth.models import User
from django.forms import ValidationError

def validate_email_unique(value):
    """Ensure email is unique across all users"""
    if User.objects.filter(email=value).exists():
        raise ValidationError("This email already exists",code="email_exists")

def validate_username_unique(value):
    """
    Validate username uniqueness.
    Note: Django enforces this at DB level, but this gives better UX
    """
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            "This username is already taken",
            code='username_exists'
        )