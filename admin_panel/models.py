from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Section(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название раздела")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Page(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="pages", verbose_name="Раздел"
    )
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    content = models.TextField(verbose_name="Содержание")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    extra_data = models.JSONField(verbose_name="Дополнительные данные", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return f"{self.title} ({self.section.name})"

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
