# Generated by Django 3.2.20 on 2023-11-01 17:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0012_rename_friends_friendship_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Private',
            new_name='PrivateChat',
        ),
    ]