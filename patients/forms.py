from django import forms
from smartcare_surgery import settings
from django.contrib.admin import widgets 
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils import timezone
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from .models import User
from datetime import datetime, time, timedelta

User = get_user_model()

from .models import Appointment, Invoice

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
    title = forms.CharField(label='Title')
    description = forms.CharField(label='Description')
    appointmentID = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        appointmentID = kwargs.pop("current_appointmentID", None)
        super(CreatePrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
        self.fields['appointmentID'].initial = appointmentID
        

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class BookAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(Q(role="doctor") | Q(role="nurse")).filter(is_active=True).order_by('name'), empty_label=None)
    patient_type = forms.ChoiceField(choices=[('NHS', 'NHS'), ('Private', 'Private')], label='Patient Type')

    class Meta:
        model = Appointment
        fields = ['date', 'appointment_time', 'doctor', 'patient_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookAppointmentForm, self).__init__(*args, **kwargs)
        time_slots = self.generate_time_slots(9, 17, 10)
        self.fields['appointment_time'] = forms.ChoiceField(choices=time_slots, label='Appointment Time')

    @staticmethod
    def generate_time_slots(start_hour, end_hour, interval_minutes):
        start_time = time(hour=start_hour)
        end_time = time(hour=end_hour)
        current_time = datetime.combine(datetime.today(), start_time)
        time_slots = []

        while current_time.time() < end_time:
            time_slots.append((current_time.strftime('%H:%M'), current_time.strftime('%H:%M')))
            current_time += timedelta(minutes=interval_minutes)

        return time_slots
        
    def clean_date(self):
        desired_date = self.cleaned_data.get('date')
        if desired_date < timezone.localdate():
            raise ValidationError("You cannot book this appointment. Please select another date.")
        return desired_date

    def clean_appointment_time(self):
        desired_time = self.cleaned_data.get('appointment_time')
        desired_date = self.cleaned_data.get('date')

        desired_time = datetime.strptime(desired_time, '%H:%M').time()
        
        if desired_date == timezone.localdate() and desired_time < timezone.localtime().time():
            raise ValidationError("You cannot book this appointment. Please select another time.")

        return desired_time

class UserUpdateForm(UserChangeForm):
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    nhs_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'NHS Number'}))
    location = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Full Name'})
        if 'password' in self.fields:
            del self.fields['password']

    class Meta:
        model = User
        fields = ['email', 'name', 'date_of_birth', 'phone_number', 'nhs_number', 'location']
        

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='New Password Confirmation', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError('Your current password was entered incorrectly. Please enter it again.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError('The two new password fields must match.')
        return new_password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()