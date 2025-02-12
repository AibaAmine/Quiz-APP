from django.db import models
from apps.users.models import CustomUser
from apps.quizzes.models import Answer, Question,Quiz


# Create your models here.

class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser,models.CASCADE,related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz,models.CASCADE,related_name='attempts')
    score = models.PositiveIntegerField(null=True,blank=True)
    attempt_time = models.DateTimeField()
    class Meta:
        db_table = "quiz_attempts"
    
class UserResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt,models.CASCADE,related_name='responses')
    question = models.ForeignKey(Question,models.CASCADE)
    selected_answer = models.ForeignKey(Answer,models.CASCADE)
    is_correct = models.BooleanField()
    class Meta:
        db_table = "user_responses"




    
    