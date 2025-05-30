# Generated by Django 5.1.6 on 2025-02-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_remove_message_subject_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=11)),
                ('signature', models.BooleanField(verbose_name='Я даю согласие на обработку моих персональных данных')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
