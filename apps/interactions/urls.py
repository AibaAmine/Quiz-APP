from django.urls import path
from .views import DislikesForQuizAPIView, LikeAPIView, DislikeAPIView, LikesForQuizAPIView

urlpatterns = [
    path('quizzes/<int:quiz_id>/like/', LikeAPIView.as_view(), name='like-quiz'),
    path('quizzes/<int:quiz_id>/dislike/', DislikeAPIView.as_view(), name='dislike-quiz'),
    path('quizzes/<int:quiz_id>/likes/', LikesForQuizAPIView.as_view(), name='quiz-likes'),
    path('quizzes/<int:quiz_id>/dislikes/', DislikesForQuizAPIView.as_view(), name='quiz-dislikes'),
]
