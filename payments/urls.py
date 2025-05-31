# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:username>/', views.book_skill, name='book_skill'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('bookings/', views.booking_details, name='booking_details'),
    path('complete/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]