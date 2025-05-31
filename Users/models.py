#models.py
#Yeamin
from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/profile_images/', default='images/profile_images/default.jpg', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone=models.CharField(default="Enter number",max_length=11,null=True, blank=True)
    status=models.CharField(default='Non-professional', max_length=100)
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} profile'

    def is_currently_banned(self):
        import datetime
        from django.utils import timezone
        if self.banned_until and self.banned_until > timezone.now():
            return True
        return False
        
    def is_banned_now(self):
        from django.utils import timezone
        now = timezone.now()
        if self.banned_until:
            if self.banned_until > now:
                return True
            else:
                
                if self.is_banned:
                    self.is_banned = False
                    self.save(update_fields=['is_banned'])
        return False


class Skill(models.Model):
    PRICE_TYPE_CHOICES = [
        ('hourly', 'Hourly Rate'),
        ('fixed', 'Fixed Price'),
    ]
    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Skill'


class SkillOption(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class PublicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="public_profile")
    rating = models.FloatField(default=0.0)
    followers = models.ManyToManyField(User, related_name="follows", blank=True)
    following = models.ManyToManyField(User, related_name="following_profiles", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Public Profile"

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()
    
    
class ProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_images")
    image = models.ImageField(upload_to='profile_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded by {self.user.username}"   
    

class Rating(models.Model):
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_received")
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    rating_value = models.PositiveSmallIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_user', 'rated_by') 

    def __str__(self):
        return f"{self.rated_by.username} rated {self.rated_user.username} - {self.rating_value}"
