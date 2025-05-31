# message/urls.py
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('message_list')), name='messages_root'),
    path('chat/<str:username>/', views.chat_interface, name='chat_interface'),
    path('read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('message_list/', views.message_list, name='message_list'),
    path('search/', views.search_users, name='search_users'),
]