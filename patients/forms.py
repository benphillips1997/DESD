from django import forms
from smartcare_surgery import settings
from django.contrib.admin import widgets 
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

User = get_user_model()

from patients.models import Appointment

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

class BookAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(role="doctor").order_by('name'), empty_label=None)

    class Meta:
        model = Appointment
        fields = ['date', 'appointment_time', 'doctor']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.DateTimeInput(attrs={'type': 'time'}),
        }
    def clean_date(self):
        desired_date = self.cleaned_data.get('date')
        if desired_date < timezone.localdate():
            raise ValidationError("You cannot book this appointment. Please select another date.")
        return desired_date

    def clean_appointment_time(self):
        desired_time = self.cleaned_data.get('appointment_time')
        desired_date = self.cleaned_data.get('date')
        
        if desired_date == timezone.localdate() and desired_time < timezone.localtime().time():
            raise ValidationError("You cannot book this appointment. Please select another time.")

        return desired_time


    
