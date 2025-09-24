from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # include all accounts routes (signup, login, logout, dashboard, role dashboards)
    path('', include('accounts.urls')),

    path('patients/', include('patients.urls', namespace='patients')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('receptionists/', include('receptionists.urls', namespace='receptionists')),

]
