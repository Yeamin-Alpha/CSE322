# payments/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:username>/', views.book_skill, name='book_skill'),
    path('payment/', views.payment_page, name='payment_page'),
    path('booking-details/', views.booking_details, name='booking_details'),  
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  
]

