# receptionists/urls.py
from django.urls import path
from . import views

app_name = 'receptionists'

urlpatterns = [
    path('', views.receptionist_list, name='receptionist_list'),
    path('add/', views.add_receptionist, name='add_receptionist'),
    path('edit/<int:pk>/', views.edit_receptionist, name='edit_receptionist'),
    path('delete/<int:pk>/', views.delete_receptionist, name='delete_receptionist'),  # delete URL
]
