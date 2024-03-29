from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # set group
        group = Group.objects.get(name=user.role.title())
        group.user_set.add(user)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    nhs_number = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('nurse', 'Nurse'), ('patient', 'Patient'), ('admin', 'Admin'), ('doctor', 'Doctor')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    location = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.email


class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="patient")
    doctor = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="doctor")
    date = models.DateField()
    appointment_time = models.TimeField()
    appointment_end_time = models.TimeField()
    PATIENT_TYPE_CHOICES = [
        ('NHS', 'NHS'),
        ('Private', 'Private'),
    ]
    patient_type = models.CharField(max_length=7, choices=PATIENT_TYPE_CHOICES, default='NHS')
    appointment_status = models.CharField(max_length=20, choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Cancelled", "Cancelled")])

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Appointment, self).save(*args, **kwargs)
        if is_new:
            Invoice.objects.create(
                appointment=self,
                date_issued=self.date,
                due_date=self.date + datetime.timedelta(days=30),
                amount=0,
                status="Unpaid"
            )

class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.RESTRICT)
    appointment = models.ForeignKey(Appointment, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Inactive", "Inactive"), ("Re-issue requested", "Re-issue requested")])


class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    date_issued = models.DateField()
    due_date = models.DateField()
    appointment = models.ForeignKey(Appointment, on_delete=models.RESTRICT)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=[("Unpaid", "Unpaid"), ("Paid", "Paid")])

class Patient(models.Model):
    userID = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    nhs_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'patients_user'

    def __str__(self):
        return self.name

class SurgeryChangeRequest(models.Model):
    nhs_number = models.CharField(max_length=20)
    relocation_date = models.DateField()
    destination = models.CharField(max_length=255)
    comments = models.TextField()

    def __str__(self):
        return f"Surgery Change Request - NHS Number: {self.nhs_number}"
