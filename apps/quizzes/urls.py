from django.urls import path
from .views import (
    CreateQuizAPIView,
    FollowedUsersQuizAPIView,
    QuizDetailAPIView,
    ListQuizzesAPIView,
    ListAllQuizzesAPIView,
)

urlpatterns = [
    path("create/", CreateQuizAPIView.as_view(), name="create-quiz"),
    path(
        "following-quizzes/",
        FollowedUsersQuizAPIView.as_view(),
        name="following-quizzes",
    ),
    path("<int:pk>/", QuizDetailAPIView.as_view(), name="quiz-detail"),
    path("", ListQuizzesAPIView.as_view(), name="quizzes"),
    path("all/", ListAllQuizzesAPIView.as_view(),name="all-quizzes"),
]
