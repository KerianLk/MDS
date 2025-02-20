from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Пациент'),
        ('doctor', 'Врач'),
        ('admin', 'Администратор'),
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    rassylka = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"