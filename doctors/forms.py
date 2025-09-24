from django import forms
from accounts.models import CustomUser
from .models import Doctor

class DoctorCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['specialization', 'contact', 'username', 'password']  # removed name and email

    def save(self, commit=True):
        username = self.cleaned_data['username']

        # Create or get the CustomUser for this doctor
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={'role': 'doctor'}
        )

        if created:
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()

        # Create or update Doctor object
        doctor, doc_created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                'specialization': self.cleaned_data['specialization'],
                'contact': self.cleaned_data['contact']
            }
        )

        if not doc_created:
            doctor.specialization = self.cleaned_data['specialization']
            doctor.contact = self.cleaned_data['contact']
            if commit:
                doctor.save()

        return doctor
