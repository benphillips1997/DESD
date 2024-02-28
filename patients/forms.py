from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name", max_length=100)
    surname = forms.CharField(label="Surname", max_length=100)
    password = forms.PasswordInput()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
