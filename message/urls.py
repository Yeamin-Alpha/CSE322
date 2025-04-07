from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:username>/', views.chat_interface, name='chat_interface'),
    path('read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('message_list/', views.message_list, name='message_list'),
    path('search/', views.search_users, name='search_users'),
]
