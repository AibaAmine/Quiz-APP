from apps.quizzes.serializers import QuizSerializer
from rest_framework import views
from rest_framework import generics
from apps.quizzes.models import Quiz
from rest_framework.permissions import IsAuthenticated

# Create your views here.


#api view to list quizzes of the authenticated user
class ListQuizzesAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        quizzes = Quiz.objects.filter(user = user)
        return quizzes
    
class CreateQuizAPIView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Automatically set the user as the logged-in user so only the  logged in user can create the quiz
        print("auth user id :",self.request.user.id)
        serializer.save(user = self.request.user)
    
class FollowedUsersQuizAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         user = self.request.user
         
         # following_users = user.following.all()
         following_users = user.following.values_list("following", flat=True) #.values_list("user", flat=True) → Extracts only the user IDs from the relation as a list.

         return Quiz.objects.filter(user__id__in=following_users) #user__id tells Django to look at the id field of the user ForeignKey.
    

# Retrieve, update, or delete a specific quiz
class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user) #ensure that a user can only retrieve, update, or delete their own quizzes






