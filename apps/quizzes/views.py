from apps.quizzes.serializers import QuizSerializer
from rest_framework import views
from rest_framework import generics
from quizzes.models import Quiz
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CreateQuizAPIView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    
class FollowedUsersQuizAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         user = self.request.user
         
         # following_users = user.following.all()
         following_users = user.following.values_list("user", flat=True) #.values_list("user", flat=True) → Extracts only the user IDs from the relation as a list.

         return Quiz.objects.filter(user__id__in=following_users) #user__id tells Django to look at the id field of the user ForeignKey.
    

# Retrieve, update, or delete a specific quiz
class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user) #ensure that a user can only retrieve, update, or delete their own quizzes



