from django import forms
from patient.models import *
from users.models import *

class AppointmentFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient','usluga', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        patient = cleaned_data.get('patient')

        # Проверяем, есть ли уже запись на это время
        #if Appointment.objects.filter(date=date, time=time,patient='patient').exists():
        #    raise forms.ValidationError("На выбранное время уже есть запись.")
        return cleaned_data


class MessageFormDoctor(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver',  'body']


