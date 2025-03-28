from django import forms
from .models import *
from users.models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import Select
from django import forms

class TimeSelectWidget(forms.Select):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.choices = self.get_time_choices()

    def get_time_choices(self):
        times = []
        for hour in range(9, 18):  # С 9 до 18
            for minute in ['00', '30']:  # Шаг 30 минут
                time_str = f"{hour:02d}:{minute}"
                times.append((time_str, time_str))  # (Значение, Подсказка)
        return times

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'usluga', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': TimeSelectWidget(),
        }

    def clean_time(self):
        time = self.cleaned_data['time']
        hour, minute = map(int, time.split(':'))
        if hour < 9 or hour >= 18:
            raise ValidationError("Записи доступны только с 9:00 до 18:00.")
        if minute not in [0, 30]:
            raise ValidationError("Записи доступны только с интервалом 30 минут.")
        return time


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
            widgets = {
            'passport_date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }




class UserDataForm(forms.ModelForm):
    # Добавляем поля из User (например, email, first_name, last_name)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','middle_name', 'last_name','date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }



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
        widgets = {
            'consent_date': forms.DateInput(attrs={'type': 'date'}),
        }

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
