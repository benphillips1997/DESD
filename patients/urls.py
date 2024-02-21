from django.urls import path
from patients import views

urlpatterns = [
    path("", views.home, name="home"),
]