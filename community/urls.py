#url:

from django.urls import path
from community import views

urlpatterns = [
    path('add-post/', views.Posts, name='add_post'),
    path('community/', views.posts_with_comments, name='community'),
    path('posts/<int:post_id>/toggle_upvote/', views.toggle_upvote, name='toggle_upvote'),
    path('notifications/', views.notifications, name='notifications'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/report/', views.report_post, name='report_post'),
    path('reports/', views.view_reports, name='view_reports'),
    path('reports/posts/<int:post_id>/delete/', views.delete_reported_post, name='delete_reported_post'),

]
