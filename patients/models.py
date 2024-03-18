from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group

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
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Cancelled", "Cancelled")])


class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.RESTRICT)
    appointment = models.ForeignKey(Appointment, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Inactive", "Inactive"), ("Re-issue requested", "Re-issue requested")])


class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.RESTRICT)
    cost = models.FloatField()
    status = models.CharField(max_length=10, choices=[("Unpaid", "Unpaid"), ("Paid", "Paid")])