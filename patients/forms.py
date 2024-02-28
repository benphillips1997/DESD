from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    location = forms.CharField()  # Hidden input to store location data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
