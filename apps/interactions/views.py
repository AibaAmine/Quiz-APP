from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.db.utils import IntegrityError
from .models import Like, Dislike
from apps.quizzes.models import Quiz

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        """Like a quiz"""
        user = request.user
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise NotFound("Quiz not found")

        try:
            like = Like.objects.create(user=user, quiz=quiz)
            return Response({"message": "Liked successfully"}, status=201)
        except IntegrityError:
            return Response({"message": "Already liked"}, status=400)

    def delete(self, request, quiz_id):
        """Unlike a quiz"""
        user = request.user
        deleted, _ = Like.objects.filter(user=user, quiz_id=quiz_id).delete()
        if deleted:
            return Response({"message": "Unliked successfully"}, status=200)
        return Response({"message": "Not liked before"}, status=400)


class DislikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        """Dislike a quiz"""
        user = request.user
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise NotFound("Quiz not found")

        try:
            dislike = Dislike.objects.create(user=user, quiz=quiz)
            return Response({"message": "Disliked successfully"}, status=201)
        except IntegrityError:
            return Response({"message": "Already disliked"}, status=400)

    def delete(self, request, quiz_id):
        """Remove dislike"""
        user = request.user
        deleted, _ = Dislike.objects.filter(user=user, quiz_id=quiz_id).delete()
        if deleted:
            return Response({"message": "Dislike removed"}, status=200)
        return Response({"message": "Not disliked before"}, status=400)
