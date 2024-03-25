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
    path("doctor_prescriptions/", views.doctor_prescriptions, name="doctor_prescriptions"),
    # path("create_prescription/", views.create_prescription, name="create_prescription"),
    path("reissue_prescription", views.reissue_prescription, name="reissue_prescription"),
    path("recent_patients/", views.recent_patients, name="recent_patients"),
    path("patient_records/", views.patient_records, name="patient_records"),
    path("current_appointment", views.current_appointment, name="current_appointment"),

    path("registrations/", views.registrations, name="registrations"),
    path("records/", views.records, name="records"),
    path("reports/", views.reports, name="reports"),
    path("operations/", views.operations, name="operations"),
    path("verify_user/", views.verify_user, name="verify_user"),

    path("book_appointment/", views.book_appointment, name="book_appointment"),
    path("request_reissue/", views.request_reissue, name="request_reissue"),
    path("patient_prescriptions/", views.patient_prescriptions, name="patient_prescriptions"),
    path("history/", views.history, name="history"),

    path('invoices/', views.patient_invoices, name='patient_invoices'),
    path('print_invoice/<int:invoice_id>/', views.print_invoice, name='print_invoice'),

    path("payments/", views.payments, name="payments"),

    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout, name="logout")
]