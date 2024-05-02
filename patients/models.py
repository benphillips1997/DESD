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
    requested_deletion = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.email


class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    date = models.DateField()
    appointment_time = models.TimeField()
    appointment_end_time = models.TimeField()
    PATIENT_TYPE_CHOICES = [
        ('NHS', 'NHS'),
        ('Private', 'Private'),
    ]
    patient_type = models.CharField(max_length=7, choices=PATIENT_TYPE_CHOICES, default='NHS')
    appointment_status = models.CharField(max_length=20, choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Cancelled", "Cancelled")])
    notes = models.TextField(null=True, blank=True)
    referral = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals")

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Appointment, self).save(*args, **kwargs)
        if is_new:
            if self.doctor.role == "doctor":
                rate_per_minute = AppointmentPrice.objects.get(priceID=1).doctor_price / 10
            elif self.doctor.role == "nurse":
                rate_per_minute = AppointmentPrice.objects.get(priceID=1).nurse_price / 10
            invoice_amount = rate_per_minute * 10
            Invoice.objects.create(
                appointment=self,
                date_issued=self.date,
                due_date=self.date + datetime.timedelta(days=30),
                amount=invoice_amount,
                status="Unpaid"
            )

class AppointmentPrice(models.Model):
    priceID = models.IntegerField(primary_key=True)
    doctor_price = models.FloatField(default=50)
    nurse_price = models.FloatField(default=30)

class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Inactive", "Inactive"), ("Re-issue requested", "Re-issue requested")])


class PrescriptionMedicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    recommended_daily_dosage = models.CharField(max_length=100, blank=True, null=True)

    def str(self):
        return self.name

    prescription_medicines = [
        ('Omeprazole', 'Proton pump inhibitors', ''),
        ('Lansoprazole', 'Proton pump inhibitors', ''),
        ('Simvastatin', 'Statins', ''),
        ('Atorvastatin', 'Statins', ''),
        ('Pravastatin', 'Statins', ''),
        ('Bisoprolol', 'Beta-Blockers', ''),
        ('Atenolol', 'Beta-Blockers', ''),
        ('Propranolol', 'Beta-Blockers', ''),
        ('Amlodipine', 'Calcium-channel blockers', ''),
        ('Felodipine', 'Calcium-channel blockers', ''),
        ('Diltiazem', 'Calcium-channel blockers', ''),
        ('Nifedipine', 'Calcium-channel blockers', ''),
        ('Lercanidipine', 'Calcium-channel blockers', ''),
        ('Cyclizine', 'H1 receptor Antagonists', ''),
        ('Cetirizine', 'H1 receptor Antagonists', ''),
        ('Loratadine', 'H1 receptor Antagonists', ''),
        ('Fexofenadine', 'H1 receptor Antagonists', ''),
        ('Chlorphenamine', 'H1 receptor Antagonists', ''),
        ('Tramadol', 'Opioids', ''),
        ('Codeine', 'Opioids', ''),
        ('Dihydrocodeine', 'Opioids', ''),
    ]


class Invoice(models.Model):
    TYPE_CHOICES = (
        ('Appointment', 'Appointment'),
        ('Prescription', 'Prescription'),
    )
    type = models.CharField(max_length=12, choices=TYPE_CHOICES, default='Appointment')
    invoiceID = models.AutoField(primary_key=True)
    date_issued = models.DateField()
    due_date = models.DateField()
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=[("Unpaid", "Unpaid"), ("Paid", "Paid")])


class SurgeryChangeRequest(models.Model):
    nhs_number = models.CharField(max_length=20)
    relocation_date = models.DateField()
    destination = models.CharField(max_length=255)
    comments = models.TextField()

    def __str__(self):
        return f"Surgery Change Request - NHS Number: {self.nhs_number}"


class WorkingSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.JSONField(default=None)