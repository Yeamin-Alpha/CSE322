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
    def __str__(self):
        return f'{self.user.username} profile'



class Skill(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=7, null=True, blank=True)


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
