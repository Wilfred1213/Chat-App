from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from chat.models import *
from chat.timestamp import format_timestamp
from django.db.models import Q, Count, Sum
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.timesince import timesince
from django.utils import timezone
from chat.onlinestatus import join_room, is_user_online
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from authentications.models import CustomUser

User=get_user_model()


def index(request):
    return render(request, 'chat/all_rooms.html', {
        'rooms': Room.objects.all(),
    })


def chatroom(request, room_name):
    current_user = request.user
    chat_room = Room.objects.get(name=room_name)
    get_room_name = chat_room.name
    get_messages = Message.objects.filter(room=chat_room)
    formatted_messages = [(message, format_timestamp(message.timestamp)) for message in get_messages]

    online_users = CustomUser.objects.all().order_by('is_online')

    # Users' friends
    try:
        friendship_instance = Friendship.objects.get(user=current_user)
        related_friends = friendship_instance.related_friends.all()
        related_friends_ordered = related_friends.order_by('-is_online')
    except Friendship.DoesNotExist:
        related_friends_ordered = []

    all_users = CustomUser.objects.exclude(id=current_user.id).exclude(id__in=related_friends.values_list('id', flat=True))

    for friend in all_users:
        friend_request = FriendRequest.objects.filter(to_user=friend, status='pending').first()
        friend.has_pending_request = friend_request is not None

    arr = []

    for friend in related_friends_ordered:
        other_user_chats = PrivateChat.objects.filter(
            sender=friend, friend=current_user, is_read_friend=False
        )
        other_user_unread_count = other_user_chats.count()
        print('coming from room', other_user_unread_count)

        arr.append((friend, other_user_unread_count))

    context = {
        'room': chat_room,
        'chats': get_messages,
        'room_name': get_room_name,
        'formatted_messages': formatted_messages,
        'all_users': all_users,
        'online': online_users,
        'friends': related_friends_ordered,
        'arr': arr,
        'current_user':current_user
    }

    return render(request, 'chat/chatroom.html', context)

def create_chat_room(request):
    user = request.user

    if request.method == 'POST':
        roomName = request.POST.get('roomName')

        if Room.objects.filter(name=roomName).exists():
            return JsonResponse({'success': False, 'message': f'"{roomName}" already exists.'})
        else:
            createRoom = Room(name=roomName)
            createRoom.save()
            createRoom.online.add(user)
            return JsonResponse({'success': True, 'message': f'Chat room "{roomName}" created successfully.'})

    return render(request, 'chat/create_room.html')



def add_friend(request, friend_id):
    friends = User.objects.filter(id = friend_id)
    
    if request.method == 'POST': 
        friendship, created = Friendship.objects.get_or_create(user=request.user)      
        for user in friends:
            # if user.id == friendship.related_friends: 
            friendship.related_friends.add( user )
                
            return JsonResponse({'success': True, 'message': f'You are now friends'})


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CustomUser):
            return str(obj)  # Use the string representation of the user
        return super().default(obj)

def chat_friend(request, friend_id):
    current_user = request.user

    try:
        selected_friend = get_object_or_404(User, id=friend_id)
              
        friendship_instance = Friendship.objects.get(user=current_user)
        related_friends_ordered = friendship_instance.related_friends.order_by('-is_online')

        all_users = User.objects.exclude(id=current_user.id).exclude(
            id__in=friendship_instance.related_friends.values_list('id', flat=True)
        )
    except User.DoesNotExist or Friendship.DoesNotExist:
        selected_friend = None
        all_users = None
        related_friends_ordered = None
        friendship_instance = None

    for friend in all_users:
        friend_request = FriendRequest.objects.filter(to_user=friend, status='pending').first()
        friend.has_pending_request = friend_request is not None

    arr = []

    for friendship in related_friends_ordered:  
        other_user_chats = PrivateChat.objects.filter(
            sender=friendship, friend=current_user, is_read_friend=False
        )
        other_user_unread_count = other_user_chats.count()

        arr.append((friendship, other_user_unread_count))

    messages = PrivateChat.objects.filter(
        Q(sender=current_user, friend=selected_friend) | Q(sender=selected_friend, friend=current_user)
    ).order_by('timestamp')

    # Process form submission to create PrivateChat objects
    if request.method == 'POST':
        chat = request.POST.get('chat')
        attach = request.POST.get('attach')
        try:
            message, created = PrivateChat.objects.get_or_create(
                sender=current_user, friend=selected_friend, 
                content=chat, is_read_friend=False,
                attachment = attach
            )
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # Construct a list of dictionaries for each message
    messages_data = []
    for message in messages:
        timesince_value = timesince(message.timestamp, timezone.now())
        messages_data.append({
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': timesince_value,
            'photo_url': message.sender.photo.url,
            
        })
       
    # adding friends
    if request.method == 'POST':
        friendship, created = Friendship.objects.get_or_create(user=current_user)
        friendship.related_friends.add(selected_friend)

        return JsonResponse({'success': True, 'message': f'You are now friends'})

    context = {
        'friends': friendship_instance,
        'frnd': selected_friend,
        'messages': messages_data,
        'all_users': all_users,
        'related_friends_ordered': related_friends_ordered,
        'selected_friend': selected_friend,
        'arr': arr,
    }

    # Check if it's an AJAX request
    if request.is_ajax():
        return JsonResponse({'success': True, 'messages': messages_data, 'unread_counts': arr}, encoder=CustomJSONEncoder)

    else:
        # Render the page for non-AJAX requests
        return render(request, 'chat/private_chat.html', context)


def friends(request):
    user = request.user
    friends = Friendship.objects.filter(user=user)
    all_users = User.objects.exclude(id=user.id).exclude(id__in=friends.values_list('related_friends__id', flat=True))

    user_count = user.sent_messages.filter(is_read_friend=False).count()
    # Create a dictionary to store unread message counts for each user
    unread_messages_counts = {}

    for friend in friends:
        for related_user in friend.related_friends.all():
            unread_messages_count = PrivateChat.objects.filter(friend=related_user, is_read_friend=False).count()
            unread_messages_counts[related_user.id] = unread_messages_count

    for user in all_users:
        friend_request = FriendRequest.objects.filter(to_user=user, status='pending').first()
        user.has_pending_request = friend_request is not None
        

    context = {
        'all_users': all_users,
        'friends': friends,
        
        'user_count':user_count,
    }
    return render(request, 'chat/friends.html', context)
  
def add_new_friend(request, to_user):
    to_user = User.objects.get(id=to_user)
    if request.method == 'POST' : 
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, 
                                                                  to_user = to_user)
       
        is_pending = friend_request.status == 'pending'
       
        return JsonResponse({'success': True, 'message': 'Friend request sent', 'pending': is_pending})
    
@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)

    if friend_request.status == 'pending':
        friend_request.status = 'accepted'
        friend_request.save()

    if friend_request.status == 'accepted':
        sender_friendship, _ = Friendship.objects.get_or_create(user=request.user)
        receiver_friendship, _ = Friendship.objects.get_or_create(user=friend_request.from_user)

        sender_friendship.related_friends.add(friend_request.from_user)
        receiver_friendship.related_friends.add(request.user)
        
        return redirect('all_request') 
    
@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    
    if friend_request.status == 'accepted':
        
        return redirect('all_request') 

def all_request(request):
    user = request.user.id
    try:
        approve_request = FriendRequest.objects.get(id = user)
    except FriendRequest.DoesNotExist:
        approve_request = None
    context = {
        'approved':approve_request,
    }
    return render(request, 'chat/friend_request.html', context)

    
def update_unread_messages(request):
    if request.method == 'POST' and request.is_ajax():
        friend_id = request.POST.get('friend_id')
        current_user = request.user

        # Mark messages as read for the specific friend if they are not already read
        unread_messages = PrivateChat.objects.filter(
            friend=current_user, sender=friend_id, is_read_friend=False
        )

        # Get the count before marking messages as read
        unread_count = unread_messages.count()


        # Additional data to include in the response
        response_data = {
            'success': True,
            'unread_count': unread_count,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

def mark_messages_as_read(request):
    if request.method == 'POST' and request.is_ajax():
        friend_id = request.POST.get('friend_id')
        current_user = request.user

        # Mark messages as read for the specific friend
        unread_messages = PrivateChat.objects.filter(friend=current_user, sender=friend_id, is_read_friend=False)
        unread_count = unread_messages.count()

        unread_messages.update(is_read_friend=True)

        # Additional data to include in the response
        response_data = {
            'success': True,
            'unread_count': unread_count,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})



def delete_message(request):
    if request.method == 'POST' and request.is_ajax():
        message_id = request.POST.get('message_id')

        try:
            message = PrivateChat.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'success': True})
        except PrivateChat.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Message not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
