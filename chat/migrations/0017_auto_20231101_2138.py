# Generated by Django 3.2.20 on 2023-11-01 20:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0016_auto_20231101_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='user',
        ),
        migrations.AddField(
            model_name='friend',
            name='user',
            field=models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
