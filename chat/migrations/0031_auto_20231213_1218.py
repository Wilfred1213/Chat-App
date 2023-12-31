# Generated by Django 3.2.20 on 2023-12-13 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0030_chatcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatcount',
            name='is_read_friend_count',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chatcount',
            name='is_read_sender_count',
            field=models.BooleanField(default=True),
        ),
    ]
