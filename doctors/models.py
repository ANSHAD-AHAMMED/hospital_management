from django.db import models
from accounts.models import CustomUser

class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    #email = models.EmailField(unique=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
