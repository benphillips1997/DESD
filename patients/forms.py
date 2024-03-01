from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('nurse', 'Nurse'), ('admin', 'Admin'), ('doctor', 'Doctor')])
    location = forms.CharField(widget=forms.HiddenInput(), required=False)   # Hidden input to store location data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
