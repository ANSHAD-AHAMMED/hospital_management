# receptionists/models.py
from django.db import models
from accounts.models import CustomUser

class Receptionist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
