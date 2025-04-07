from django.db import models

# payments/models.py

from django.db import models
from django.contrib.auth.models import User
from Users.models import Skill
from django.utils import timezone

class Booking(models.Model):
    skill_user = models.ForeignKey(User, related_name="received_bookings", on_delete=models.CASCADE) 
    booked_by = models.ForeignKey(User, related_name="made_bookings", on_delete=models.CASCADE)  
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    booking_date = models.DateField(default=timezone.now) 
    booking_status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Confirmed')

    def __str__(self):
        return f"Booking by {self.booked_by.username} for {self.skill.name} with {self.skill_user.username}"


