from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', views.create_chat_room, name = 'create'),
    path('room/<str:room_name>/', views.chatroom, name = 'room'),
    path('add_friend/<int:friend_id>/', views.add_friend, name = 'add_friend'),
    
    path('chat_friend/<int:friend_id>/', views.chat_friend, name = 'chat_friend'),
    path('friends/', views.friends, name = 'friends'),
    path('add_new_friend/<int:to_user>/', views.add_new_friend, name = 'add_new_friend'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name = 'accept_friend_request'),
    path('all_request/', views.all_request, name = 'all_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name = 'accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name = 'reject_friend_request'),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('delete_message/', views.delete_message, name='delete_message'),
    path('update_unread_messages/', views.update_unread_messages, name='update_unread_messages'),
    # path('get_unread_count/<int:friend_id>/',  views.get_unread_count, name='get_unread_count'),
    

]