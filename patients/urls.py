from django.urls import path
from patients import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),

    path("patient_login/", views.patient_login, name="patient_login"),
    path("doctor_login/", views.doctor_login, name="doctor_login"),
    path("nurse_login/", views.nurse_login, name="nurse_login"),
    path("admin_login/", views.admin_login, name="admin_login"),

    path("patient_signup/", views.patient_signup, name="patient_signup"),
    path("doctor_signup/", views.doctor_signup, name="doctor_signup"),
    path("nurse_signup/", views.nurse_signup, name="nurse_signup"),
    path("admin_signup/", views.admin_signup, name="admin_signup"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("weekly_schedule/", views.weekly_schedule, name="weekly_schedule"),
    path("prescriptions/", views.prescriptions, name="prescriptions"),
    path("recent_patients/", views.recent_patients, name="recent_patients"),
    path("patient_records/", views.patient_records, name="patient_records"),
    path("invoices/", views.invoices, name="invoices"),
    path("history/", views.history, name="history"),
    path("payments/", views.payments, name="payments"),

    path("registrations/", views.registrations, name="registrations"),
    path("records/", views.records, name="records"),
    path("reports/", views.reports, name="reports"),
    path("operations/", views.operations, name="operations"),
    path("verify_user/", views.verify_user, name="verify_user"),

    path("book_appointment/", views.book_appointment, name="book_appointment"),

    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout, name="logout")
]