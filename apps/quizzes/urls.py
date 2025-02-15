from django.urls import path
from .views import CreateQuizAPIView, FollowedUsersQuizAPIView, QuizDetailAPIView

urlpatterns = [
    path("create/", CreateQuizAPIView.as_view(), name="create-quiz"),
    path("following-quizzes/", FollowedUsersQuizAPIView.as_view(), name="following-quizzes"),
     path('quizzes/new/', CreateQuizAPIView.as_view(), name='quiz-create'),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
]
