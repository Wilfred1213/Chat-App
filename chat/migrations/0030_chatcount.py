# Generated by Django 3.2.20 on 2023-12-12 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0029_rename_is_read_privatechat_is_read_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read_sender_count', models.IntegerField(default=0)),
                ('is_read_friend_count', models.IntegerField(default=0)),
                ('chat', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='chat.privatechat')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
