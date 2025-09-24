from django.urls import path

from patients.urls import app_name
from . import views

app_name='reports'

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('patients/', views.patients_report, name='patients_report'),
    path('doctors/', views.doctors_report, name='doctors_report'),
    path('appointments/', views.appointments_report, name='appointments_report'),
    path('billing/', views.billing_report, name='billing_report'),
]
