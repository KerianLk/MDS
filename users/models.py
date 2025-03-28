from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Пациент'),
        ('doctor', 'Врач'),
        ('admin', 'Администратор'),
    )
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="Телефон")
    rassylka = models.BooleanField(default=False, verbose_name="Разрешаю присылать мне сообщения со спец. предложениями")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    email = models.EmailField(unique=True, verbose_name="Почта")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient', verbose_name="Роль")
    photo = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватарка")

    def __str__(self):
        return f"{self.get_full_name()}"