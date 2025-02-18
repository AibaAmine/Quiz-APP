from django.urls import path
from .views import LikeAPIView, DislikeAPIView

urlpatterns = [
    path('quizzes/<int:quiz_id>/like/', LikeAPIView.as_view(), name='like-quiz'),
    path('quizzes/<int:quiz_id>/dislike/', DislikeAPIView.as_view(), name='dislike-quiz'),
]
