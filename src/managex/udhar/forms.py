from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 10)
    password = forms.CharField(widget = forms.PasswordInput)
