#accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model  # <-- add this
from patients.models import Patient, Banner
from doctors.models import Doctor
from appointments.models import Appointment
from billing.models import Bill
from .forms import CustomUserCreationForm


# Role check functions
def is_admin(user):
    return user.role == 'admin'

def is_doctor(user):
    return user.role == 'doctor'

def is_patient(user):
    return user.role == 'patient'

def is_receptionist(user):
    return user.role == 'receptionist'

# Signup view
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password1,
            role='patient'
        )

        # Create Patient if it doesn't already exist
        Patient.objects.get_or_create(
            user=user,
            defaults={
                'name': username,
                'username': username,
                #'gender': gender
            }
        )

        messages.success(request, "Signup successful! You can now login.")
        return redirect('login')

    return render(request, 'accounts/signup.html')



# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # added role selection

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Redirect based on role
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'doctor':
                return redirect('doctor_dashboard')
            elif role == 'patient':
                return redirect('patient_dashboard')
            elif role == 'receptionist':
                return redirect('receptionist_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')

# Logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Unified dashboard (optional)
@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        return redirect('patient_dashboard')
    elif request.user.role == 'receptionist':
        return redirect('receptionist_dashboard')
    else:
        messages.error(request, "Unauthorized access!")
        return redirect('login')

# Role dashboards
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_bills': Bill.objects.count(),
    }
    return render(request, 'accounts/dashboards/admin_dashboard_new.html', context)

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'accounts/dashboards/doctor_dashboard.html')

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    banners = Banner.objects.all().order_by('-created_at')  # Fetch banners
    return render(request, 'accounts/dashboards/patient_dashboard.html', {'banners': banners})

@login_required
@user_passes_test(is_receptionist)
def receptionist_dashboard(request):
    return render(request, 'accounts/dashboards/receptionist_dashboard.html')
