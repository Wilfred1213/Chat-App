from django.urls import path, include
from . import views

app_name = 'authentications'
urlpatterns = [
    path('signup/', views.register_user, name = 'signup'),
    path('loggin/', views.loggin, name = 'loggin'),
    path('logout/', views.logout, name='logout')
    
]