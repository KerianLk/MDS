from django import forms
from .models import *
from users.models import *
from django.core.validators import RegexValidator
class AppointmentFormPatient(forms.ModelForm):
    #date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.ChoiceField(choices=[])
    class Meta:
        model = Appointment
        fields = ['doctor','usluga', 'date', 'time']
        widgets = {
             'date': forms.DateInput(attrs={'type': 'date'}),
        #     'time': forms.TimeInput(attrs={'type': 'time'}),
         }

    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop('available_slots', [])
        super().__init__(*args, **kwargs)
        self.fields['time'].choices = [(slot, slot.strftime("%H:%M")) for slot in available_slots]
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        doctor = cleaned_data.get('doctor')

        # Проверяем, есть ли уже запись на это время
        #if Appointment.objects.filter(date=date, time=time,doctor='doctor').exists():
        #    raise forms.ValidationError("На выбранное время уже есть запись.")
        #return cleaned_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'body']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        # Фильтрация пользователей в зависимости от роли текущего пользователя
        if current_user.role == 'doctor':
            self.fields['receiver'].queryset = User.objects.filter(role='patient')
        elif current_user.role == 'patient':
            self.fields['receiver'].queryset = User.objects.filter(role='doctor')

class FeedbackForm(forms.ModelForm):
    soglasie = forms.BooleanField(required=True)
    number = forms.CharField(min_length=11, max_length=11, validators=[
        RegexValidator(
            regex=r'^\d+$',
            message='Поле должно содержать только числа.',
            code='invalid_number'
        )
    ])
    class Meta:
        model = Feedback
        fields = ['name', 'number', 'email','message','soglasie']



class UserProfileForm(forms.ModelForm):
    snils = forms.CharField(min_length=11, max_length=11, validators=[
        RegexValidator(
            regex=r'^\d+$',
            message='Поле должно содержать только числа.',
            code='invalid_number'
        )
    ])
    passport_series = forms.CharField(min_length=4, max_length=4,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Поле должно содержать только числа.',
                code='invalid_number'
            )
        ])
    passport_number = forms.CharField(min_length=6, max_length=6,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Поле должно содержать только числа.',
                code='invalid_number'
            )
        ])
    class Meta:
            model = UserProfile
            fields = ['avatar', 'snils', 'dms', 'gender', 'passport_series', 'passport_number', 'passport_date_of_issue', 'passport_issued_by', 'passport_photo1', 'passport_photo2']




class UserDataForm(forms.ModelForm):
    # Добавляем поля из User (например, email, first_name, last_name)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','middle_name', 'last_name','date_of_birth']



class PatientSurveyForm(forms.ModelForm):
    class Meta:
        model = PatientSurvey
        fields = ['question1', 'question2', 'question3', 'question4', 'question5']


class MedicalConsentForm(forms.ModelForm):
    signature = forms.BooleanField(required=True)
    passport_series = forms.CharField(min_length=4, max_length=4,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Поле должно содержать только числа.',
                code='invalid_number'
            )
        ])
    passport_number = forms.CharField(min_length=6, max_length=6,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Поле должно содержать только числа.',
                code='invalid_number'
            )
        ])
    class Meta:
        model = MedicalConsent
        fields = ['full_name', 'passport_series', 'passport_number', 'passport_issued_by', 'address', 'consent_date', 'signature']

class OrderCallForm(forms.ModelForm):
    phone = forms.CharField(min_length=11, max_length=11,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Поле должно содержать номер телефона.',
                code='invalid_number'
            )
        ])
    signature = forms.BooleanField(required=True)
    class Meta:
        model = OrderCall
        fields = ['name', 'phone','signature']
