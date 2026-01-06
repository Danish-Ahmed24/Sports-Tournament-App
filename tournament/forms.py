# tournament/forms.py
from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[("PLAYER", "Player")])
    name = forms.CharField(max_length=100)
    experience = forms.IntegerField(min_value=0)