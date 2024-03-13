from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label='')
    email = forms.EmailField(label='')
    first_name = forms.CharField(label='')
    surname = forms.CharField(label='')
    password = forms.CharField(widget=forms.PasswordInput, label='')

    location = forms.CharField(widget=forms.HiddenInput(), required=False)   # Hidden input to store location data

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['surname'].widget.attrs.update({'placeholder': 'Surname'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})  

class LoginForm(forms.Form):
    email = forms.EmailField(label='')
    password = forms.CharField(widget=forms.PasswordInput, label='')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class CreatePrescriptionForm(forms.Form):
    title = forms.CharField(label='')
    description = forms.CharField(label='')

    def __init__(self, *args, **kwargs):
        super(CreatePrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})