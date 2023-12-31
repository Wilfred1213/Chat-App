from django.contrib import admin
from chat.models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(PrivateChat)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
