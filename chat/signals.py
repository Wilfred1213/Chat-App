from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Room, PrivateChat
from django.contrib.auth.signals import user_logged_in, user_logged_out

User = get_user_model()

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # This signal will be triggered whenever a User instance is saved
    # You can use this to update the online status of users in the Room model
    print(f"User logged in: {user}")
    if user and not user.is_online:
        user.is_online = True
        user.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    print(f"User logged out: {user}")
    if user and user.is_online:
        user.is_online = False
        user.save()

# Connect the user_logged_out signal to the user_logged_out_handler
user_logged_in.connect(user_logged_in_handler)
user_logged_out.connect(user_logged_out_handler)