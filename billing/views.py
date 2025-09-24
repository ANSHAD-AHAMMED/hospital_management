from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bill
from .forms import BillForm
from patients.models import Patient
from appointments.models import Appointment

@login_required
def bill_list(request):
    if request.user.role in ['admin', 'receptionist']:
        bills = Bill.objects.all()
    elif request.user.role == 'patient':
        if hasattr(request.user, "patient_profile"):
            bills = Bill.objects.filter(patient=request.user.patient_profile)
        else:
            messages.error(request, "No patient profile linked to this account.")
            return redirect('dashboard')
    else:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    return render(request, 'billing/bill_list.html', {'bills': bills})

@login_required
def add_bill(request):
    if request.user.role not in ['admin', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill created successfully!")
            return redirect('billing:bill_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BillForm()

    return render(request, 'billing/add_bill.html', {'form': form})



@login_required
def edit_bill(request, pk):
    if request.user.role not in ['admin', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill updated successfully!")
            return redirect('billing:bill_list')
    else:
        form = BillForm(instance=bill)
    return render(request, 'billing/edit_bill.html', {'form': form})

@login_required
def delete_bill(request, pk):
    if request.user.role not in ['admin', 'receptionist']:
        messages.error(request, "Access denied")
        return redirect('dashboard')
    bill = get_object_or_404(Bill, pk=pk)
    bill.delete()
    messages.success(request, "Bill deleted successfully!")
    return redirect('billing:bill_list')
