from django import forms
from accounts.models import CustomUser
from .models import Receptionist

class ReceptionistCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Receptionist
        fields = ['contact', 'username', 'password']  # removed name and email

    def save(self, commit=True):
        username = self.cleaned_data['username']

        # Create or get the CustomUser for this receptionist
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={'role': 'receptionist'}
        )

        if created:
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()

        # Create or update Receptionist object
        receptionist, rec_created = Receptionist.objects.get_or_create(
            user=user,
            defaults={
                'contact': self.cleaned_data['contact']
            }
        )

        if not rec_created:
            receptionist.contact = self.cleaned_data['contact']
            if commit:
                receptionist.save()

        return receptionist
