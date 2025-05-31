#Yeamin
#url:

from django.urls import path
from Users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup_page, name="signup"),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.Ulogout, name='logout'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('activate-professional-mode/', views.activate_professional_mode, name='activate_professional_mode'),
    path('add-skill/', views.Skills, name='add_skill'),
    path('delete_skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('view-skills/', views.view_skill, name='view_skill'),
    path('public_profile/<str:username>/', views.public_profile, name='public_profile'),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('filter-skills/', views.filter_skills, name='filter_skills'),
    path('services/', views.services_page, name='services_page'),
    path('rate/<str:username>/', views.submit_rating, name='submit_rating'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('search/', views.search, name='search'),
    path('delete_rating/<str:username>/', views.delete_rating, name='delete_rating'), 
    path('profile/<str:username>/following/', views.following_page, name='following_page'),
    path('profile/<str:username>/followers/', views.followers_page, name='followers_page'),
    path('ban_user/<str:username>/', views.ban_user, name='ban_user'),
    path('unban_user/<str:username>/', views.unban_user, name='unban_user'),
]
