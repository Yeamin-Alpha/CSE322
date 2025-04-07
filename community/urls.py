#url:

from django.urls import path
from community import views

urlpatterns = [
    path('add-post/', views.Posts, name='add_post'),
    path('community/', views.posts_with_comments, name='community'),
    path('posts/<int:post_id>/toggle_upvote/', views.toggle_upvote, name='toggle_upvote'),
    path('notifications/', views.notifications, name='notifications'),

]
