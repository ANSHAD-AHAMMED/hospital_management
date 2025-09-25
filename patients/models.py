# patients/models.py
from django.db import models
from accounts.models import CustomUser


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
        ('Prefer not to say','Prefer not to say')
    ])
    contact = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  # new field
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name
#patients\models.py
class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title