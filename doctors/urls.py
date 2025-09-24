from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('add/', views.add_doctor, name='add_doctor'),           # Only admin
    path('edit/<int:pk>/', views.edit_doctor, name='edit_doctor'), # Only admin
    path('delete/<int:pk>/', views.delete_doctor, name='delete_doctor'), # Only admin
]
