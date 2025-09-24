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

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role='patient'
        )
        patient = Patient.objects.create(
            user=user,
            age=self.cleaned_data['age'],
            gender=self.cleaned_data['gender'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone']
        )
        return patient



class PatientForm(forms.ModelForm):
    """ Used for editing patient details (not login credentials). """
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'address', 'phone']
