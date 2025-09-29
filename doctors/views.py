from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Doctor
from .forms import DoctorCreateForm
from accounts.views import is_admin
from django.urls import reverse

@login_required
@user_passes_test(is_admin)
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


@login_required
@user_passes_test(is_admin)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor created successfully!")
            return redirect('doctors:doctor_list')
    else:
        form = DoctorCreateForm()

    return render(request, 'doctors/add_doctor.html', {
        'form': form,
        'back_url': reverse('doctors:doctor_list')  # ✅ use reverse instead of hardcoding
    })

@login_required
@user_passes_test(is_admin)
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorCreateForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor updated successfully!")
            return redirect('doctors:doctor_list')
    else:
        form = DoctorCreateForm(instance=doctor)
    return render(request, 'doctors/edit_doctor.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.user.delete()  # Delete CustomUser first
    doctor.delete()
    messages.success(request, "Doctor deleted successfully!")
    return redirect('doctors:doctor_list')
