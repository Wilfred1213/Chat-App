# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        if user not in self.online.all():
            self.online.add(user)
            self.save()

    def leave(self, user):
        if user in self.online.all():
            self.online.remove(user)
            self.save()


    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'
    

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null = True, related_name='chatmessages')
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, null = True)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    


class Friend(models.Model):
    # note that we have to add user directly when they signup
    user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE, null = True)
    
    
    def __str__(self):
        
        return f"Chat between {self.user}"

    
class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    related_friends = models.ManyToManyField(User, related_name='related_friendships')
    timestamp = models.DateTimeField(auto_now_add=True)
       
class PrivateChat(models.Model):
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content= models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
   
    is_read_sender = models.BooleanField(default=True)
    is_read_friend = models.BooleanField(default=False)
    attachment = models.ImageField(upload_to ='attachments', null= True, blank=True)

    def __str__(self):
        
        return f"Message from {self.sender} to {self.friend} at {self.timestamp}"
    
   
class FriendRequest(models.Model):
    STATUS = (
        ('recieved', 'Received'),
        ('pending', 'Pending'),
        ('reject', 'Reject')
    )
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def __str__(self):
        return f'{self.from_user} send friend request to {self.to_user}--- status --{self.status}'
    
