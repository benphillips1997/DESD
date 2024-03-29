from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages

from .forms import BookAppointmentForm, SignUpForm, LoginForm, CreatePrescriptionForm, PatientSearchForm
from .models import Prescription, Invoice, Appointment, Patient

from .forms import BookAppointmentForm, SignUpForm, LoginForm, CreatePrescriptionForm, UserUpdateForm, PasswordChangeForm
from .models import Prescription, Invoice, Appointment

from django.http import JsonResponse
from smartcare_surgery import settings as project_settings
from django.utils import timezone
from django.utils.timezone import localdate, make_aware
import datetime
from time import localtime

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

            # check for duplicate users
            all_users = User.objects.all()
            # form = SignUpForm()
            message = " is already used for an account"
            for user in all_users:
                if username == user.userID:
                    message = "UserID" + message
                    return render(request, f"patients/signup.html", {'form': form, 'role': user_role, 'error': message})
                if email == user.email:
                    message = "Email" + message
                    return render(request, f"patients/signup.html", {'form': form, 'role': user_role, 'error': message})

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


# sets any 'scheduled' appointments that are in the past to 'completed'
def check_appointment_status():
    all_appointments = Appointment.objects.all()
    for appointment in all_appointments:
        if appointment.appointment_status == "Scheduled":
            now = datetime.datetime.now()
            if (appointment.date < datetime.date.today()) or (appointment.date <= datetime.date.today() and appointment.appointment_end_time < now.time()):
                appointment.appointment_status = "Completed"
                appointment.save()

    
@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        check_appointment_status()
        if user.role == "doctor" or user.role == "nurse":
            all_appointments = Appointment.objects.filter(doctor=user.userID)
            now = datetime.date.today()
            appointments_today = all_appointments.filter(date=now).order_by("appointment_time")
            next_appointment = appointments_today.filter(appointment_status="Scheduled").first()
            completed_appointments = appointments_today.filter(appointment_status='Completed').count()
            remaining_appointments = appointments_today.filter(appointment_status='Scheduled').count()
            return render(request, f"patients/{user.role}_dashboard.html", {"user": user, "appointments": appointments_today, 
                                    "next_appointment": next_appointment, "completed_appointments": completed_appointments, "scheduled_appointments": remaining_appointments})
        elif user.role == "admin":
            appointments_today = Appointment.objects.filter(date=datetime.date.today())
            completed_appointments = appointments_today.filter(appointment_status='Completed').count()
            remaining_appointments = appointments_today.filter(appointment_status='Scheduled').count()
            return render(request, f"patients/{user.role}_dashboard.html", {"user": user, "completed_appointments": completed_appointments, "scheduled_appointments": remaining_appointments})
        else:
            return render(request, f"patients/{user.role}_dashboard.html", {"user": user})
    else:
        return redirect("user_login", user_role=user.role)


@login_required
def weekly_schedule(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    check_appointment_status()
    # retrive all appointments for the next week
    all_appointments = Appointment.objects.filter(doctor=request.user.userID)
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    
    weekly_appointments = all_appointments.filter(date__range=(today, next_week)).order_by("date", "appointment_time")
    
    return render(request, "patients/weekly_schedule.html", {"appointments": weekly_appointments})

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
def current_appointment(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    now = datetime.datetime.now()
    # retrieve appointment that is within the current 10 minuter time slot
    start_time = now - datetime.timedelta(minutes=now.minute % 10, seconds=now.second, microseconds=now.microsecond)
    current_appointment = Appointment.objects.filter(doctor=request.user.userID).filter(date=datetime.date.today()).filter(appointment_time=(start_time.time())).first()
    message = ""
    if request.method == "POST":
        form = CreatePrescriptionForm(request.POST)
        if form.is_valid():
            appointmentID = form.cleaned_data["appointmentID"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"] 

            appointment = Appointment.objects.get(appointmentID=appointmentID)

            patient = appointment.patient

            new_prescription = Prescription.objects.create(patient=patient, appointment=appointment, title=title, description=description, status="Active")
            new_prescription.save()

            message = "Added prescription"
    else:
        if current_appointment:
            form = CreatePrescriptionForm(current_appointmentID=current_appointment.appointmentID)
        else:
            form = CreatePrescriptionForm()
    return render(request, "patients/current_appointment.html", {"form": form, "current_appointment": current_appointment, "message": message})

@login_required
def recent_patients(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    check_appointment_status()
    # retrive all appointments in the last year
    all_appointments = Appointment.objects.filter(doctor=request.user.userID)
    today = datetime.date.today()
    time_before = today - datetime.timedelta(weeks=4)
    recent_appointments = all_appointments.filter(date__range=(time_before, today), appointment_status="Completed").order_by("date")
    message = ""
    if request.method == "POST":
        form = CreatePrescriptionForm(request.POST, auto_id=True)
        if form.is_valid():
            appointmentID = form.cleaned_data["appointmentID"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"] 

            appointment = Appointment.objects.get(appointmentID=appointmentID)

            patient = appointment.patient

            new_prescription = Prescription.objects.create(patient=patient, appointment=appointment, title=title, description=description, status="Active")
            new_prescription.save()

            message = f"Added prescription {title} for {patient.name}"
    else:
        form = CreatePrescriptionForm(auto_id=True)
    return render(request, "patients/recent_patients.html", {"appointments": recent_appointments, "form": form, "message": message})


@login_required
def patient_records(request):
    if not (request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='Nurse').exists()):
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/patient_records.html")

@login_required
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoiceID=invoice_id)
    appointment = invoice.appointment
    rate_per_minute = 0

    start_datetime = make_aware(datetime.datetime.combine(appointment.date, appointment.appointment_time))
    end_datetime = make_aware(datetime.datetime.combine(appointment.date, appointment.appointment_end_time))
    duration_timedelta = end_datetime - start_datetime
    duration_minutes = int(duration_timedelta.total_seconds() / 60)

    if invoice.appointment.doctor.role == "doctor":
        rate_per_minute = 5
    elif invoice.appointment.doctor.role == "nurse":
        rate_per_minute = 3
            
    invoice.amount = duration_minutes * rate_per_minute

    patient_location = appointment.patient.location
    practitioner_name = appointment.doctor.name
    practitioner_role = appointment.doctor.get_role_display()

    context = {
        'invoice': invoice,
        'duration_minutes': duration_minutes,
        'rate_per_minute': rate_per_minute,
        'patient_location': patient_location,
        'practitioner_name': practitioner_name,
        'practitioner_role': practitioner_role
    }
    return render(request, 'patients/print_invoice.html', context)

@login_required
def patient_invoices(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    user_invoices = Invoice.objects.filter(appointment__patient=request.user).order_by('-date_issued')
    for invoice in user_invoices:
        start_time = invoice.appointment.appointment_time
        end_time = invoice.appointment.appointment_end_time
        start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
        end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)
        duration_timedelta = end_datetime - start_datetime
        duration_minutes = int(duration_timedelta.total_seconds() / 60)
        invoice.duration = duration_minutes

        if invoice.appointment.doctor.role == "doctor":
            rate_per_minute = 5
        elif invoice.appointment.doctor.role == "nurse":
            rate_per_minute = 3
            
        invoice.amount = duration_minutes * rate_per_minute
        
    return render(request, "patients/patient_invoices.html", {'user_invoices': user_invoices})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_invoices(request):
    all_invoices = Invoice.objects.all().order_by('-date_issued')
    for invoice in all_invoices:
        start_time = invoice.appointment.appointment_time
        end_time = invoice.appointment.appointment_end_time
        start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
        end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)
        duration_timedelta = end_datetime - start_datetime
        duration_minutes = int(duration_timedelta.total_seconds() / 60)
        invoice.duration = duration_minutes

        if invoice.appointment.doctor.role == "doctor":
            rate_per_minute = 5
        elif invoice.appointment.doctor.role == "nurse":
            rate_per_minute = 3
        
        invoice.amount = f"£{duration_minutes * rate_per_minute:.2f}"
        
    return render(request, "patients/admin_invoices.html", {'all_invoices': all_invoices})

@login_required
def visit_history(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")

    appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_status="Completed"
    ).order_by('-date')

    return render(request, "patients/visit_history.html", {'appointments': appointments})


@login_required
def payments(request):
    if not request.user.groups.filter(name='Patient').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    return render(request, "patients/payments.html")

@login_required
def registrations(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to view this page.")
    
    unverified_patients = User.objects.filter(role='patient', is_active=False)
    unverified_doctors = User.objects.filter(role='doctor', is_active=False)
    unverified_nurses = User.objects.filter(role='nurse', is_active=False)

    # Pass the filtered users to the context
    context = {
        "unverified_patients": unverified_patients,
        "unverified_doctors": unverified_doctors,
        "unverified_nurses": unverified_nurses,
    }
    
    return render(request, "patients/registrations.html", context)
@login_required
def verify_user(request):
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

def is_staff_member(user):
    return user.groups.filter(name__in=['Doctor', 'Nurse', 'Admin']).exists() or user.is_staff

@login_required
def records(request):
    query = request.GET.get('query')
    patients = None

    if query:
        patients = Patient.objects.filter(name__icontains=query, role='patient').values(
            'userID', 'email', 'name', 'date_of_birth', 'phone_number', 'nhs_number', 'role', 'is_active', 'location'
        )

    return render(request, 'patients/patient_records.html', {
        'patients': patients,
        'query': query
    })


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
def patient_settings(request):
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'update_settings':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = PasswordChangeForm(user=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('patient_settings')
        elif 'action' in request.POST and request.POST['action'] == 'change_password':
            p_form = PasswordChangeForm(request.user, request.POST)
            u_form = UserUpdateForm(instance=request.user)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Your password has been updated.')
                return redirect('patient_settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PasswordChangeForm(user=request.user)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'patients/patient_settings.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'patients/patient_settings.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        if request.session.get('confirm_delete', False):
            user = request.user
            user.is_active = False
            user.save()
            logout(request)
            return redirect('home')
        else:
            request.session['confirm_delete'] = True
            return redirect('home')
    request.session.pop('confirm_delete', None)
    return redirect('home')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            desired_time = form.cleaned_data['appointment_time']
            desired_date = form.cleaned_data['date']
            doctor = form.cleaned_data['doctor']
            duration = datetime.timedelta(minutes=10)

            # Check for overlapping appointments
            if Appointment.objects.filter(Q(date=desired_date) & Q(appointment_time=desired_time), doctor=doctor).exists():
                messages.error(request, "This time slot is already booked. Please choose another.")
                message = "This time slot is already booked. Please choose another."
                return render(request, 'patients/book_appointment.html', {'form': form, 'message': message})
            
            start_datetime = datetime.datetime.combine(desired_date, desired_time)
            end_datetime = start_datetime + duration
            end_time = end_datetime.time()

            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                date=desired_date,
                appointment_time=desired_time,
                appointment_end_time=end_time,
                patient_type=form.cleaned_data['patient_type'],
                appointment_status='Scheduled'
            )
            appointment.save()

            message = f"Successfully booked appointment at {str(desired_date)} {str(desired_time)} with {doctor.name}"
            return render(request, 'patients/book_appointment.html', {'form': form, 'message': message})
    else:
        form = BookAppointmentForm()
    return render(request, 'patients/book_appointment.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")