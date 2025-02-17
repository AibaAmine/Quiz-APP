from django.db import models
from apps.users.models import CustomUser

# Create your models here. 


class Quiz(models.Model):

    class DifficultyChoices(models.TextChoices):
        EASY = 'Easy'
        MEDIUM = 'Medium'
        HARD = 'Hard'
    
    user = models.ForeignKey(CustomUser,models.CASCADE,related_name='quizzes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20,choices=DifficultyChoices,default=DifficultyChoices.EASY)
    category = models.CharField(max_length=100)
    #sub_category = models.CharField(max_length=20)
    is_public = models.BooleanField(default=True)
    timer_seconds = models.PositiveIntegerField(null=True,blank=True)
    attempt_limit = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "quizzes"
    
    
class Question(models.Model):
    
     quiz = models.ForeignKey(Quiz,models.CASCADE,related_name='questions')
     question_text = models.TextField()
     question_type = models.CharField(max_length=20)
     created_at = models.DateTimeField(auto_now_add=True)
     is_ai_generated = models.BooleanField(default=False)
     is_correct = models.BooleanField(default=False)
     class Meta:
        db_table = "questions"

class Answer(models.Model):
    question = models.ForeignKey(Question,models.CASCADE,related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default = False)
    class Meta:
        db_table = "answers"
        



