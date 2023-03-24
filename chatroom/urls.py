from django.urls import path
from home import views as home_views
from . import views

urlpatterns = [
    path('chats/', views.chat_view, name='chatroom' ),
    path('chats/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/user/<int:pk>', views.user_list, name='user-detail'),
    path('api/users/', views.user_list, name = 'user-list'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
]
