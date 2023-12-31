from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null = True)
    photo = models.ImageField(upload_to='media', null = True)
    is_online = models.BooleanField(default=False)
      
    
    class Meta(AbstractUser.Meta):
        # swappable = 'authentications.CustomUser'
    
        app_label = 'authentications'
    
    def __str__(self):
        return self.username