from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    num_comments = models.IntegerField(default=0)
    num_upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post by {self.user.username} - Upvotes: {self.num_upvotes}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on Post ID {self.post.id}"


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upvotes')

    class Meta:
        unique_together = ('user', 'post')  # Ensures a user can upvote a post only once

    def __str__(self):
        return f"Upvote by {self.user.username} on Post ID {self.post.id}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification[:20]}..."
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on Post ID {self.post.id} - Reason: {self.reason}"
