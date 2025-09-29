from django.db import models
from accounts.models import CustomUser

class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"
