from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from .forms import LoginForm 

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

            user = User.objects.create_user(userID=username, email=email, password=password, role=role, name=f"{first_name} {surname}")
            user.role = role
            user.save()

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, "patients/sign_up.html", {'form': form})

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return render(request, f"patients/{user.role}_dashboard.html", {"user": user})
    else:
        return redirect("user_login")
    

def weekly_schedule(request):
    return render(request, "patients/weekly_schedule.html")

def prescriptions(request):
    return render(request, "patients/prescriptions.html")

def recent_patients(request):
    return render(request, "patients/recent_patients.html")

def patient_records(request):
    return render(request, "patients/patient_records.html")

def invoices(request):
    return render(request, "patients/invoices.html")

def history(request):
    return render(request, "patients/history.html")

def payments(request):
    return render(request, "patients/payments.html")

def registrations(request):
    return render(request, "patients/registrations.html")

def records(request):
    return render(request, "patients/records.hmtl")

def reports(request):
    return render(request, "patients/reports.hmtl")

def operations(request):
    return render(request, "patients/operations.hmtl")

def settings(request):
    return render(request, "patients/settings.html")

def book_appointment(request):
    return render(request, "patients/book_appointment.html")

def logout(request):
    auth_logout(request)
    return redirect("user_login")