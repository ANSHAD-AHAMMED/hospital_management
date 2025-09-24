# patients/urls.py
from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='patient_list'),             # /patients/
    path('add/', views.add_patient, name='add_patient'),           # /patients/add/
    path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),  # /patients/edit/1/
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient')  # /patients/delete/1/
]
