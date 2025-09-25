from django import forms
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from .models import Doctor

class DoctorCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Doctor
        fields = ['specialization', 'contact', 'username', 'password']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)
        # Populate username if editing an existing doctor
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = CustomUser.objects.filter(username=username)
        if self.instance and self.instance.pk:
            # Exclude current user when checking uniqueness
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data.get('password')

        if self.instance and self.instance.pk:  # Editing existing doctor
            user = self.instance.user
            user.username = username
            if password:
                user.set_password(password)
            if commit:
                user.save()

            doctor = self.instance
            doctor.specialization = self.cleaned_data['specialization']
            doctor.contact = self.cleaned_data['contact']
            if commit:
                doctor.save()

        else:  # Creating a new doctor
            user = CustomUser(username=username, role='doctor')
            if password:
                user.set_password(password)
            if commit:
                user.save()

            doctor = Doctor(
                user=user,
                specialization=self.cleaned_data['specialization'],
                contact=self.cleaned_data['contact']
            )
            if commit:
                doctor.save()

        return doctor
