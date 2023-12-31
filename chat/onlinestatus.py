from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def join_room(user, room_name):
    user.is_online = True
    user.save()

    # Assuming room_name is the user ID, update the user with that ID
    room_id =(room_name)
    room = CustomUser.objects.get(pk=room_id)
    room.is_online = True
    room.save()

def is_user_online(user, room_name):
    # Assuming room_name is the user ID, check the online status of the user with that ID
    room_id = int(room_name)
    return CustomUser.objects.get(pk=room_id).is_online
