# Generated by Django 3.2.20 on 2023-11-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_friendship_related_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='related_friends',
            field=models.ManyToManyField(related_name='related_friendships', to='chat.Friend'),
        ),
    ]
