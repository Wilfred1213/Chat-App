# Generated by Django 3.2.20 on 2023-11-21 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0025_remove_friendship_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatechat',
            name='is_read',
            field=models.BooleanField(default=True),
        ),
    ]
