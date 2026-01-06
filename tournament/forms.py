# tournament/forms.py
from dataclasses import fields
from django import forms
from .validators import validate_email_unique,validate_username_unique
from tournament.models import CustomUser, Manager, Player

class BasicSignUpForm(forms.ModelForm):
    username=forms.CharField(max_length=30, required=True,validators=[validate_username_unique])
    email=forms.EmailField(required=True,validators=[validate_email_unique])
    password=forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)

    class Meta:
        model = CustomUser
        fields=['name','experience','role']

class ManagerSignUpForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields=['teamName']

class PlayerSignUpForm(forms.ModelForm):
    class Meta:
        model = Player
        fields=['position','age']