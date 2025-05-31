# payments/models.py
from django.db import models
from django.contrib.auth.models import User
from Users.models import Skill
from django.utils import timezone

class Booking(models.Model):
    skill_user = models.ForeignKey(User, related_name="received_bookings", on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, related_name="made_bookings", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Cancelled', 'Cancelled'),
            ('Completed', 'Completed'),
        ],
        default='Pending',  
    )
    booking_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.booked_by.username} for {self.skill.name} with {self.skill_user.username}"

    def calculate_total(self):
        if self.skill.price_type == 'hourly' and self.hours:
            return self.skill.price * self.hours
        print(self.skill.price, self.skill.price_type)
        return self.skill.price

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def complete_booking(self):
        self.booking_status = 'Completed'
        self.booking_completed = True
        self.save()

    def cancel_booking(self):
        self.booking_status = 'Cancelled'
        self.save()