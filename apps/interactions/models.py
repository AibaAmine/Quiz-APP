from django.db import models
from apps.quizzes.models import Quiz
from apps.users.models import CustomUser


# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "likes"
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "comments"
    
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ratings")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField()
    class Meta:
        db_table = "ratings"
    

class Follower(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
         db_table = "followers"
         unique_together = ('follower', 'following')  # Prevents duplicate follows

        



