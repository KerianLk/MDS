from django.db import models
from users.models import *



class Appointment(models.Model):
    USLUGA_CHOICES = (
        ('сonsultation', 'Консультация'),
        ('treatment', 'Лечение'),
        ('operation', 'Операция'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'}, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    usluga = models.CharField(max_length=100, choices=USLUGA_CHOICES, default='сonsultation')
    status = models.CharField(max_length=255, default='wait')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.get_full_name()} on {self.date} at {self.time}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'},related_name='medical_records')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    images = models.ImageField(upload_to='medical_records/', blank=True, null=True)

    def __str__(self):
        return f"Record for {self.patient.get_full_name()} by Dr. {self.doctor.get_full_name()}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.get_full_name()} to {self.receiver.get_full_name()}"


class Feedback(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    soglasie = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.name} ({self.email})"

from django.conf import settings
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Девушка'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male', verbose_name="Пол")
    snils = models.CharField(max_length=11, blank=True, null=True, verbose_name="СНИЛС")
    dms = models.CharField(max_length=50, blank=True, null=True, verbose_name="ДМС")
    passport_series = models.CharField(max_length=4, verbose_name="Серия паспорта",blank=True, null=True)
    passport_number = models.CharField(max_length=6, verbose_name="Номер паспорта",blank=True, null=True)
    passport_date_of_issue = models.DateField(verbose_name="Дата выдачи",blank=True, null=True)
    passport_issued_by = models.CharField(max_length=255, verbose_name="Кем выдан",blank=True, null=True)
    passport_photo1 = models.ImageField(upload_to='passport_photos/', blank=True, null=True, verbose_name="Фото паспорта 1")
    passport_photo2 = models.ImageField(upload_to='passport_photos/', blank=True, null=True, verbose_name="Фото паспорта 2")

    def __str__(self):
        return f'Профиль {self.user.first_name} {self.user.last_name}'


class PatientSurvey(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey')
    question1 = models.TextField(verbose_name="Были у вас когда-либо аллергические реакции", )
    question2 = models.TextField(verbose_name="Есть у вас хронические заболевания")
    question3 = models.TextField(verbose_name="Страдаете ли заболеваниями полости рта")
    question4 = models.TextField(verbose_name="Есть в вашей семье аллергические реакции ")
    question5 = models.TextField(verbose_name="Есть ли у вас особенности")
    completed = models.BooleanField(default=False, verbose_name="Заполнена")

    def __str__(self):
        return f'Анкета {self.user.first_name} {self.user.last_name}'


class MedicalConsent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medical_consent')  # Связь с пользователем
    # Поля для данных пользователя
    full_name = models.CharField(verbose_name="Я, ",max_length=255)  # ФИО
    passport_series = models.CharField(verbose_name="паспорт: серия:",max_length=4)  # Серия паспорта
    passport_number = models.CharField(verbose_name=" номер :",max_length=6)  # Номер паспорта
    passport_issued_by = models.CharField(verbose_name="выдан ",max_length=255)  # Кем выдан
    address = models.CharField(verbose_name="проживающий по адресу ",max_length=512)  # Адрес
    consent_date = models.DateField(verbose_name="Дата ")  # Дата согласия
    signature = models.BooleanField(verbose_name="Подписать электронной подписью")
    # Подпись (можно сохранить как изображение или текст)
    # Дата создания и изменения
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Согласие на медицинское вмешательство: {self.user.username}"

class OrderCall(models.Model):
    name = models.CharField( max_length=255)
    phone = models.CharField(max_length=11)
    signature = models.BooleanField(verbose_name="Я даю согласие на обработку моих персональных данных")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Заказать звонок: {self.phone}"
