#appointments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm, AppointmentRequestForm
from patients.models import Patient
from doctors.models import Doctor
from accounts.models import CustomUser


@login_required
def appointment_list(request):
    # Admins and receptionists see all appointments
    if request.user.role in ['admin', 'receptionist']:
        appointments = Appointment.objects.all()

    # Doctors see only their own appointments
    elif request.user.role == 'doctor':
        if hasattr(request.user, 'doctor_profile'):
            appointments = Appointment.objects.filter(doctor=request.user.doctor_profile)
        else:
            messages.error(request, "Doctor profile not found.")
            return redirect('dashboard')

    # Patients see only their own approved or pending appointments
    elif request.user.role == 'patient':
        if hasattr(request.user, 'patient_profile'):
            appointments = Appointment.objects.filter(
                patient=request.user.patient_profile
            ).exclude(request_status='Rejected')  # hide rejected requests
        else:
            messages.error(request, "Patient profile not found.")
            return redirect('dashboard')

    else:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments
    })



@login_required
def add_appointment(request):
    if request.user.role not in ['admin', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')  # "2025-09-23"
        time = request.POST.get('time')  # "10:57"
        reason = request.POST.get('reason')

        Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )
        messages.success(request, "Appointment created successfully!")
        return redirect('appointments:appointment_list')

    return render(request, 'appointments/add_appointment.html', {
        'patients': patients,
        'doctors': doctors
    })

@login_required
def edit_appointment(request, pk):
    if request.user.role not in ['admin', 'receptionist', 'doctor']:
        messages.error(request, "Access denied")
        return redirect('dashboard')
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/edit_appointment.html', {'form': form})

@login_required
def delete_appointment(request, pk):
    if request.user.role not in ['admin', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect('appointments:appointment_list')


# appointments/views.py
@login_required
def request_appointment(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied")
        return redirect('dashboard')

    patient = request.user.patient_profile

    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.request_status = 'Pending'
            appointment.save()
            messages.success(request, "Appointment request sent successfully!")
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentRequestForm()

    # Get all doctors
    doctors = CustomUser.objects.filter(role='doctor').select_related('doctor_profile')

    # Get distinct specializations from DoctorProfile
    specializations = (
        doctors
        .exclude(doctor_profile__isnull=True)
        .values_list('doctor_profile__specialization', flat=True)
        .distinct()
    )

    return render(request, 'appointments/request_appointment.html', {
        'form': form,
        'doctors': doctors,
        'specializations': specializations,
    })


@login_required
def manage_requests(request):
    if request.user.role not in ['admin', 'doctor', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    if request.user.role == 'doctor':
        requests = Appointment.objects.filter(doctor=request.user.doctor_profile, request_status='Pending')
    else:
        requests = Appointment.objects.filter(request_status='Pending')

    return render(request, 'appointments/manage_requests.html', {'requests': requests})


@login_required
def approve_request(request, pk):
    if request.user.role not in ['admin', 'doctor', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.request_status = 'Approved'
    appointment.save()
    messages.success(request, "Appointment request approved!")
    return redirect('appointments:manage_requests')


@login_required
def reject_request(request, pk):
    if request.user.role not in ['admin', 'doctor', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.request_status = 'Rejected'
    appointment.save()
    messages.success(request, "Appointment request rejected!")
    return redirect('appointments:manage_requests')

