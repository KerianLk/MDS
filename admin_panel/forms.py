from django import forms
from .models import Section, Page
from users.models import User
from patient.models import Appointment

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "slug"]

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["section", "title", "content","extra_data", "slug"]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Пароль")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'email', 'role', 'rassylka', 'date_of_birth', 'password']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'usluga', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }