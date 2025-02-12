from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

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


