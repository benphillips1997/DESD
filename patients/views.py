from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from .forms import LoginForm 
from django.http import JsonResponse


User = get_user_model()

def home(request):
    return render(request, "patients/home.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'patients/login.html', {'form': form, 'error': 'Account is disabled.'})
            else:
                return render(request, 'patients/login.html', {'form': form, 'error': 'Invalid login credentials.'})
    else:
        form = LoginForm()
    return render(request, 'patients/login.html', {'form': form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["surname"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data['role']
            location = form.cleaned_data.get('location')

            active = True
            if role == "doctor" or role == "nurse":
                active = False
            # Create the user account
            user = User.objects.create_user(userID=username, email=email, password=password, role=role, name=f"{first_name} {surname}", is_active=active)
            # Here, handle the location data as needed, e.g., saving to user profile
            user.save()

            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('dashboard')
            else:
                return redirect("user_login")
    else:
        form = SignUpForm()
    return render(request, "patients/sign_up.html", {'form': form})
    
@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return render(request, f"patients/{user.role}_dashboard.html", {"user": user})
    else:
        return redirect("user_login")
    
@login_required
def weekly_schedule(request):
    return render(request, "patients/weekly_schedule.html")

@login_required
def prescriptions(request):
    return render(request, "patients/prescriptions.html")

@login_required
def recent_patients(request):
    return render(request, "patients/recent_patients.html")

@login_required
def patient_records(request):
    return render(request, "patients/patient_records.html")

@login_required
def invoices(request):
    return render(request, "patients/invoices.html")

@login_required
def history(request):
    return render(request, "patients/history.html")

@login_required
def payments(request):
    return render(request, "patients/payments.html")

@login_required
def registrations(request):
    all_users = User.objects.all()
    unverified_users = []
    for user in all_users:
        if not user.is_active:
            unverified_users.append(user)
    return render(request, "patients/registrations.html", {"unverified_users": unverified_users})

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
        return JsonResponse(status=400)

@login_required
def records(request):
    return render(request, "patients/records.html")

@login_required
def reports(request):
    return render(request, "patients/reports.html")

@login_required
def operations(request):
    return render(request, "patients/operations.html")

@login_required
def settings(request):
    return render(request, "patients/settings.html")

@login_required
def book_appointment(request):
    return render(request, "patients/book_appointment.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect("user_login")