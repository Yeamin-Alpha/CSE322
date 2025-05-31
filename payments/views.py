# payments/views.py
from .models import Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from Users.models import Skill
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
@login_required
def book_skill(request, username):
    skill_user = get_object_or_404(User, username=username)

    if request.user == skill_user:
        messages.error(request, "You cannot book your own service")
        return redirect('profile')

    skills = Skill.objects.filter(user=skill_user)

    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        selected_skill = get_object_or_404(Skill, id=skill_id)
        
        hours = request.POST.get('hours', None)
        
       
        if selected_skill.price_type == 'hourly' and not hours:
            messages.error(request, "Please specify the number of hours required")
            return redirect('book_skill', username=username)
            
        try:
            hours = int(hours) if hours else None
        except ValueError:
            hours = None
            
        
        booking = Booking.objects.create(
            skill_user=skill_user,
            booked_by=request.user,
            skill=selected_skill,
            hours=hours,
            booking_date=timezone.now().date(),
        )

        booking.total_amount = booking.calculate_total()
        booking.save()

        return redirect('payment_page', booking_id=booking.id)

    context = {
        'skill_user': skill_user,
        'skills': skills,
    }
    return render(request, 'book_skill.html', context)
@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        booking.is_paid = True  # ✅ Mark as paid
        booking.save()

        messages.success(request, f"Payment initiated successfully using {payment_method}. Booking is now confirmed.")
        return redirect('booking_details')

    return render(request, 'payment_page.html', {'booking': booking})


@login_required
def booking_details(request):
    user = request.user

    bookings = Booking.objects.filter(
        Q(booked_by=user) | 
        Q(skill_user=user, is_paid=True)  
    ).order_by('-id')

    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_details.html', context)

@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, skill_user=request.user)
    booking.complete_booking()
    messages.success(request, "Booking completed successfully.")
    return redirect('booking_details')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, skill_user=request.user)
    booking.cancel_booking()
    messages.success(request, "Booking has been cancelled successfully.")
    return redirect('booking_details')