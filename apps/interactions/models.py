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
        unique_together = ('user', 'quiz')  # A user can like a quiz only once
        
class Dislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="quiz_dislikes")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'dislikes'
        unique_together = ('user', 'quiz')  # A user can like a quiz only once
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "comments"
    
class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comment_likes')
    comment = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='c_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'comment-likes'
        unique_together = ('user', 'comment')  # A user can like a comment only once

class Follower(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
         db_table = "followers"
         unique_together = ('follower', 'following')  # Prevents duplicate follows

        



