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
    path("reissue_prescription", views.reissue_prescription, name="reissue_prescription"),
    path("unissue_prescription", views.unissue_prescription, name="unissue_prescription"),
    path("recent_patients/", views.recent_patients, name="recent_patients"),
    path("current_appointment", views.current_appointment, name="current_appointment"),
    path('change-surgery-request/', views.change_surgery_request, name='change_surgery_request'),

    path("registrations/", views.registrations, name="registrations"),
    path("records/", views.records, name="records"),
    path("reports/", views.reports, name="reports"),
    path("operations/", views.operations, name="operations"),
    path("verify_user/", views.verify_user, name="verify_user"),
    path("verify_deletion/", views.verify_deletion, name="verify_deletion"),    
    path("delete_patient/", views.delete_patient, name="delete_patient"),
    path("change_price_doctor/", views.change_price_doctor, name="change_price_doctor"),
    path("change_price_nurse/", views.change_price_nurse, name="change_price_nurse"),
    path("remove_appointment/", views.remove_appointment, name="remove_appointment"),

    path("book_appointment/", views.book_appointment, name="book_appointment"),
    path("request_reissue/", views.request_reissue, name="request_reissue"),
    path("patient_prescriptions/", views.patient_prescriptions, name="patient_prescriptions"),
    path("payments/", views.payments, name="payments"),
    path("pay_verify/", views.pay_verify, name="pay_verify"),
    path("pay/", views.pay, name="pay"),

    path("visit_history/", views.visit_history, name="visit_history"),

    path('invoices/', views.patient_invoices, name='patient_invoices'),
    path('print_appointment_invoice/<int:invoice_id>/', views.print_appointment_invoice, name='print_appointment_invoice'),
    path('print_prescription_invoice/<int:invoice_id>/', views.print_prescription_invoice, name='print_prescription_invoice'),
    path('admin_invoices/', views.admin_invoices, name='admin_invoices'),

    path("settings/", views.patient_settings, name="patient_settings"),
    path('delete_account/', views.delete_account, name='delete_account'),
    
    path("logout/", views.logout, name="logout")
]