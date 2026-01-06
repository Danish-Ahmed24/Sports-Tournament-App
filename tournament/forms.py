from django import forms
from django.contrib.auth.models import User
from tournament.models import Player

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Player
        fields = ['experience', 'role']
