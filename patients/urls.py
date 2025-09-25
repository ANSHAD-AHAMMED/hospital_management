from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient URLs
    path('', views.patient_list, name='patient_list'),  # /patients/
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),  # /patients/dashboard/

    # Patient management
    path('add/', views.add_patient, name='add_patient'),  # /patients/add/
    path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),  # /patients/edit/1/
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),  # /patients/delete/1/

    # Banner URLs
    # Patients can only view banners
    path('banners/', views.banner_list, name='banner_list'),  # /patients/banners/

    # Admin & Receptionist can add/edit/delete banners
    path('banners/add/', views.patient_banner_add, name='patient_banner_add'),
    path('banners/edit/<int:pk>/', views.patient_banner_edit, name='patient_banner_edit'),
    path('banners/delete/<int:pk>/', views.patient_banner_delete, name='patient_banner_delete'),
]
