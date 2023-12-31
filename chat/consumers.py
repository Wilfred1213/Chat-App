import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from datetime import datetime

from chat.models import *
from chat.timestamp import format_timestamp
from chat.friendservice import FriendshipService



class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None 
        self.timestamp = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.timestamp = format_timestamp(datetime.now())
        self.accept()

        # Send previous messages to the client when they connect
        messages = Message.objects.filter(room=self.room)
        for message in messages:
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'user': message.user.username,
                'message': message.content,
                'timestamp': format_timestamp(message.timestamp),
                'photo_url': message.user.photo.url,
            }))

        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if not self.user.is_authenticated:
            return

        # Send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
                'timestamp': self.timestamp,
                'photo_url': self.user.photo.url,
            }
        )

        # Save the message to the database
        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))




# private chat 


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.friend_username = self.scope['url_route']['kwargs']['friend_username']
        self.room_group_name = f'private_chat_{self.friend_username}'

        self.user = self.scope['user']
        self.timestamp = format_timestamp(datetime.now())

        if not self.user.is_authenticated:
            await self.close()
        else:
            await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        # Instead of validating the chat, directly send the message to the group
        await self.create_private_chat_message(message)

    async def create_private_chat_message(self, message):
        try:
            friend_user = await self.get_friend_user()
        except get_user_model().DoesNotExist:
            return

        private_chat_message = await self.save_private_chat_message(friend_user, message)

        # Send the chat message event to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
                'timestamp': self.timestamp,
                'photo_url': self.user.photo.url,
            }
        )

    async def get_friend_user(self):
        return await sync_to_async(get_user_model().objects.get)(username=self.friend_username)

    async def save_private_chat_message(self, friend_user, message):
        return await sync_to_async(PrivateChat.objects.create)(
            sender=self.user,
            friend=friend_user,
            content=message
        )

    async def chat_message(self, event):
        message_data = {
            'user': event['user'],
            'content': event['message'],
            'timestamp': event['timestamp'],
            'photo_url': event['photo_url'],
        }
        await self.send(text_data=json.dumps(message_data))


