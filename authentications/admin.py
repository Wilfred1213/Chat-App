from django.contrib import admin
from authentications.models import CustomUser


# admin.py
# admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# User = get_user_model()

# # admin.py
# # from django import forms
# # from django.contrib import admin
# # from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# # from .models import CustomUser

# class CustomUserAdminForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'

#     def clean_is_online(self):
#         is_online = self.cleaned_data.get('is_online')
#         if is_online and not self.instance.is_online:
#             self.instance.is_online = True
#             self.instance.save()
#         elif not is_online and self.instance.is_online:
#             self.instance.is_online = False
#             self.instance.save()
#         return is_online

# class CustomUserAdmin(BaseUserAdmin):
#     form = CustomUserAdminForm

# # Unregister the default User model
# # admin.site.unregister(get_user_model())

# # Register the custom user model
# admin.site.register(CustomUser, CustomUserAdmin)


# # Register your models here.
admin.site.register(CustomUser)

# class CustomUserAdmin(BaseUserAdmin):
#     form = CustomUserAdminForm
#     list_display = ['username', 'email', 'is_online']