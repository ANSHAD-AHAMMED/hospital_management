from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Patient
from .forms import PatientCreationForm, PatientForm
from accounts.models import CustomUser


# ✅ Signup view (only for patients)
def signup_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('patients:signup')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role='patient'
        )
        Patient.objects.create(user=user)
        messages.success(request, "Account created! You can now log in.")
        return redirect('login')

    return render(request, 'patients/signup.html')


# ✅ Admin/Receptionist: Add patient with credentials
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def add_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully!")
            return redirect('patients:patient_list')
    else:
        form = PatientCreationForm()
    return render(request, 'patients/add_patient.html', {'form': form})


# ✅ List all patients
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist', 'doctor'])
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


# ✅ Edit patient (by admin/receptionist)
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient updated successfully!")
            return redirect('patients:patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit_patient.html', {'form': form})

# ✅ delete patient (by admin/receptionist)
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        patient.delete()
        messages.success(request, "Patient deleted successfully.")
        return redirect('patients:patient_list')  # adjust to your patient list page

    return render(request, "patients/confirm_delete.html", {"patient": patient})