# Generated by Django 3.2.20 on 2023-11-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_alter_customuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]