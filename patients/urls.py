from django.urls import path
from patients import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("user_login/", views.user_login, name="user_login"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("weekly_schedule/", views.weekly_schedule, name="weekly_schedule"),
    path("prescriptions/", views.prescriptions, name="prescriptions"),
    path("recent_patients/", views.recent_patients, name="recent_patients"),
    path("patient_records/", views.patient_records, name="patient_records"),
    path("invoices/", views.invoices, name="invoices"),
    path("settings/", views.settings, name="settings"),
]