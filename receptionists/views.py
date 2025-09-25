# receptionists/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReceptionistCreateForm
from .models import Receptionist
from django.contrib import messages

def add_receptionist(request):
    if request.method == 'POST':
        form = ReceptionistCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Receptionist added successfully!")
            return redirect('receptionists:receptionist_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReceptionistCreateForm()
    return render(request, 'receptionists/add_receptionist.html', {'form': form})


def receptionist_list(request):
    receptionists = Receptionist.objects.all()
    return render(request, 'receptionists/receptionist_list.html', {'receptionists': receptionists})

def edit_receptionist(request, pk):
    receptionist = get_object_or_404(Receptionist, pk=pk)
    if request.method == 'POST':
        form = ReceptionistCreateForm(request.POST, instance=receptionist)
        if form.is_valid():
            form.save()
            messages.success(request, "Receptionist updated successfully!")
            return redirect('receptionists:receptionist_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReceptionistCreateForm(instance=receptionist)
    return render(request, 'receptionists/edit_receptionist.html', {'form': form, 'receptionist': receptionist})


def delete_receptionist(request, pk):
    try:
        receptionist = Receptionist.objects.get(pk=pk)
    except Receptionist.DoesNotExist:
        messages.error(request, "Receptionist not found.")
        return redirect('receptionists:receptionist_list')

    if request.method == 'POST':
        user = receptionist.user
        receptionist.delete()
        user.delete()
        messages.success(request, "Receptionist deleted successfully!")
        return redirect('receptionists:receptionist_list')