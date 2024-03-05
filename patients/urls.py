from django.urls import path
from patients import views

urlpatterns = [
    # direct to home if these are visited
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("user_login/", views.home, name="home"),
    path("signup/", views.home, name="home"),

    path("user_login/<user_role>", views.user_login, name="user_login"),
    path("signup/<user_role>", views.signup, name="signup"),

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