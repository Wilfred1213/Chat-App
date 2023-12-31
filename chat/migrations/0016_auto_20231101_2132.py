# Generated by Django 3.2.20 on 2023-11-01 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0015_auto_20231101_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='user',
        ),
        migrations.AddField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]