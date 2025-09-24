from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()   # ✅ Add this
    status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Scheduled'
    )
    reason = models.TextField(null=True, blank=True)  # from earlier fix

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date} at {self.time}"
