from django.urls import path
from . import views

app_name='billing'

urlpatterns = [
    path('', views.bill_list, name='bill_list'),
    path('add/', views.add_bill, name='add_bill'),
    path('edit/<int:pk>/', views.edit_bill, name='edit_bill'),
    path('delete/<int:pk>/', views.delete_bill, name='delete_bill'),
]
