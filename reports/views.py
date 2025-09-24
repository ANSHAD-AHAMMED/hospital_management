from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import is_admin, is_receptionist
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from billing.models import Bill

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def reports_dashboard(request):
    return render(request, 'reports/reports_dashboard.html')

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def patients_report(request):
    patients = Patient.objects.all()
    return render(request, 'reports/patients_report.html', {'patients': patients})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def doctors_report(request):
    doctors = Doctor.objects.all()
    return render(request, 'reports/doctors_report.html', {'doctors': doctors})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def appointments_report(request):
    appointments = Appointment.objects.all()
    return render(request, 'reports/appointments_report.html', {'appointments': appointments})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def billing_report(request):
    bills = Bill.objects.all()
    return render(request, 'reports/billing_report.html', {'bills': bills})
