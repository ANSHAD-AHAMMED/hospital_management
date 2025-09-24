from django.urls import path
from . import views

app_name='appointments'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.add_appointment, name='add_appointment'),
    path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('request/', views.request_appointment, name='request_appointment'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('reject/<int:pk>/', views.reject_request, name='reject_request'),
]
