from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Patient, Banner
from .forms import PatientCreationForm, PatientForm
from accounts.models import CustomUser

# ✅ Signup view (only for patients)
def signup_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('patients:signup_patient')

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


# ✅ Delete patient (by admin/receptionist)
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'receptionist'])
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        patient.delete()
        messages.success(request, "Patient deleted successfully.")
        return redirect('patients:patient_list')
    return render(request, "patients/confirm_delete.html", {"patient": patient})


# ✅ Patient dashboard: show banners (read-only for patients)
@login_required
def patient_dashboard(request):
    banners = Banner.objects.all().order_by('-created_at')
    return render(request, 'accounts/dashboards/patient_dashboard.html', {'banners': banners})


# Banner Views for Admin/Receptionist
def is_admin_or_receptionist(user):
    return user.role in ['admin', 'receptionist']



@login_required
@user_passes_test(is_admin_or_receptionist)
def patient_banner_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')

        if image:
            Banner.objects.create(title=title, image=image)
            messages.success(request, "Banner added successfully!")
            return redirect('patients:banner_list')

    return render(request, 'patients/add_banner.html')


# Banner list: all users can view, admin/receptionist can manage
@login_required
def banner_list(request):
    banners = Banner.objects.all().order_by('-created_at')
    return render(request, 'patients/banner_list.html', {'banners': banners})


@login_required
@user_passes_test(is_admin_or_receptionist)
def patient_banner_edit(request, pk):
    banner = get_object_or_404(Banner, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', banner.title)
        image = request.FILES.get('image')

        banner.title = title
        if image:
            banner.image = image
        banner.save()
        messages.success(request, "Banner updated successfully!")
        return redirect('patients:banner_list')

    return render(request, 'patients/add_banner.html', {'banner': banner})


@login_required
@user_passes_test(is_admin_or_receptionist)
def patient_banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, "Banner deleted successfully!")
        return redirect('patients:banner_list')
    return render(request, 'patients/confirm_delete_banner.html', {'banner': banner})
