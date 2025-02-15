from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# todo add profile pic and bio fields
class CustomUser(AbstractUser):
    class Meta:
         db_table = "users"
    ROLE_CHOICES = [
        ('STUDENT','Student'),
        ('TEACHER','Teacher'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='STUDENT')
    
    def __str__(self):
        return self.username


class Follower(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
         db_table = "followers"
         unique_together = ('follower', 'following')  # Prevents duplicate follows


