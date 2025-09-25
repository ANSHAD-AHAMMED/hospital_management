from django import forms
from .models import Patient
from accounts.models import CustomUser


class PatientCreationForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Patient
        fields = ['username', 'password', 'age', 'gender', 'address', 'phone']

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another.")
        return username

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # Create or get user
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={'role': 'patient'}
        )
        if created:
            user.set_password(password)
            user.save()

        # Create or update patient
        patient, created_patient = Patient.objects.get_or_create(user=user)

        # Always update details
        patient.age = self.cleaned_data['age']
        patient.gender = self.cleaned_data['gender']
        patient.address = self.cleaned_data['address']
        patient.phone = self.cleaned_data['phone']
        if commit:
            patient.save()

        return patient


class PatientForm(forms.ModelForm):
    """ Used for editing patient details (not login credentials). """
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'address', 'phone']
