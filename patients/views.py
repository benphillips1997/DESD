from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib import messages
from .forms import BookAppointmentForm, SignUpForm, LoginForm, CreatePrescriptionForm
from .models import Prescription, Invoice, Appointment
from django.http import JsonResponse
from smartcare_surgery import settings as project_settings
from django.utils import timezone

User = get_user_model()

def home(request):
    return render(request, "patients/home.html")

def user_login(request, user_role):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    if user.role == user_role:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        return render(request, 'patients/login.html', {'form': form, 'error': f'Account is not a {user_role}.', 'role': user_role})
                else:
                    return render(request, 'patients/login.html', {'form': form, 'error': 'Account is disabled.', 'role': user_role})
            else:
                return render(request, 'patients/login.html', {'form': form, 'error': 'Invalid login credentials.', 'role': user_role})
    else:
        form = LoginForm()
        if user_role not in ['doctor', 'nurse', 'admin', 'patient']:
            return redirect('home')
    return render(request, f'patients/login.html', {'form': form, 'role': user_role})

def signup(request, user_role):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["surname"]
            password = form.cleaned_data["password"]
            role = user_role
            location = form.cleaned_data.get('location')

            active = True
            if role == "doctor" or role == "nurse":
                active = False
            user = User.objects.create_user(userID=username, email=email, password=password, role=role, name=f"{first_name} {surname}", is_active=active, location=location)
            user.save()

            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('dashboard')
            else:
                return redirect("user_login", user_role=role)
    else:
        form = SignUpForm()
        if user_role not in ['doctor', 'nurse', 'admin', 'patient']:
            return redirect('home')
    return render(request, f"patients/signup.html", {'form': form, 'role': user_role})

    
@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return render(request, f"patients/{user.role}_dashboard.html", {"user": user})
    else:
        return redirect("user_login", user_role=user.role)
    
@login_required
def weekly_schedule(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/weekly_schedule.html")

@login_required
def doctor_prescriptions(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    all_prescriptions = Prescription.objects.all()
    return render(request, "patients/doctor_prescriptions.html", {"requested_prescriptions": all_prescriptions})

@login_required
def reissue_prescription(request):
    if request.method == "POST":
        prescriptionID = request.POST.get("data")
        prescription = Prescription.objects.get(prescriptionID=prescriptionID)
        prescription.status = "Active"
        prescription.save()

        return JsonResponse({"prescriptionID": prescriptionID, "prescription_name": prescription.title, "user_name": prescription.patient.name}, status=200)
    else:
        return HttpResponseForbidden("You cannot access this.")

@login_required
def patient_prescriptions(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    users_prescriptions = []
    all_prescriptions = Prescription.objects.all()
    # filter the prescriptions for the logged in user
    for prescription in all_prescriptions:
        if prescription.patient == request.user:
            users_prescriptions.append(prescription)
    return render(request, "patients/patient_prescriptions.html", {'user_prescriptions': users_prescriptions})

@login_required
def request_reissue(request):
    if request.method == "POST":
        prescriptionID = request.POST.get("data")
        prescription = Prescription.objects.get(prescriptionID=prescriptionID)
        prescription.status = "Re-issue requested"
        prescription.save()

        return JsonResponse({"prescriptionID": prescriptionID, "prescription_name": prescription.title}, status=200)
    else:
        return HttpResponseForbidden("You cannot access this.")

@login_required
def create_prescription(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    if request.method == "POST":
        form = CreatePrescriptionForm(request.POST)
        if form.is_valid():
            # patientID = form.cleaned_data["patient"]
            # appointmentID = form.cleaned_data["appointment"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            patient = User.objects.get(userID="patient1")
            doctor = User.objects.get(userID="doctor1")

            appointment = Appointment.objects.create(patient=patient, doctor=doctor, appointment_time=timezone.now(), appointment_status="Completed")
            appointment.save()
            # appointment = Appointment.objects.filter(appointmentID=)

            new_prescription = Prescription.objects.create(patient=patient, appointment=appointment, title=title, description=description, status="Active")
            new_prescription.save()

            return redirect("doctor_prescriptions")
    else:
        form = CreatePrescriptionForm()
    return render(request, "patients/create_prescription.html", {"form": form})

@login_required
def recent_patients(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/recent_patients.html")

@login_required
def patient_records(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/patient_records.html")

@login_required
def invoices(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/invoices.html")

@login_required
def history(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/history.html")

@login_required
def payments(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/payments.html")

@login_required
def registrations(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    all_users = User.objects.all()
    unverified_users = []
    for user in all_users:
        if not user.is_active:
            unverified_users.append(user)
    return render(request, "patients/registrations.html", {"unverified_users": unverified_users})

@login_required
def verify_user(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    if request.method == "POST":
        userID = request.POST.get("data")

        # activate user
        success = False
        all_users = User.objects.all()
        for user in all_users:
            if userID == user.userID:
                success = True
                user.is_active = True
                user.save()

        return JsonResponse({"success": success, "userID": userID}, status=200)
    else:
        return HttpResponseForbidden("You cannot access this.")

@login_required
def records(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/records.html")

@login_required
def reports(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/reports.html")

@login_required
def operations(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/operations.html")

@login_required
def settings(request):
    return render(request, "patients/settings.html")

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            desired_start = form.cleaned_data['start_time']
            desired_end = form.cleaned_data['end_time']
            desired_date = form.cleaned_data['date']

            # Check for overlapping appointments
            overlapping_appointments = Appointment.objects.filter(
                Q(appointment_time__date=desired_date),
                (Q(start_time__lt=desired_end) & Q(end_time__gt=desired_start))
            ).exists()

            if overlapping_appointments:
                messages.error(request, "This time slot is already booked. Please choose another.")
                return render(request, 'patients/book_appointment.html', {'form': form})
                
            # No overlapping appointments, proceed to save
            form.save()
            return redirect('appointments_success')
    else:
        form = BookAppointmentForm()
    return render(request, 'patients/book_appointment.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")