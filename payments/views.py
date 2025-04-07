from django.shortcuts import render

# payments/views.py
from .models import Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from Users.models import Skill
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def book_skill(request, username):
    skill_user = get_object_or_404(User, username=username)
    
    if request.user == skill_user:
        return redirect('profile')

    skills = Skill.objects.filter(user=skill_user)
    booking_date = timezone.now().date()

    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        selected_skill = Skill.objects.get(id=skill_id)
        
        
        Booking.objects.create(
            skill_user=skill_user,
            booked_by=request.user,
            skill=selected_skill,
            booking_date=booking_date
        )

        
        return redirect('payment_page')

    context = {
        'skill_user': skill_user,
        'skills': skills,
        'booking_date': booking_date,
    }
    return render(request, 'book_skill.html', context)
@login_required
def payment_page(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
       
        messages.success(request, f"Payment completed successfully using {payment_method}.")
        return redirect('profile')  

    return render(request, 'payment_page.html') 

@login_required
def booking_details(request):
    
    bookings = Booking.objects.filter(skill_user=request.user)

    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_details.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, skill_user=request.user)

    
    booking.booking_status = 'Cancelled'
    booking.save()

    messages.success(request, "Booking has been cancelled successfully.")
    return redirect('booking_details')

