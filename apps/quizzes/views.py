from apps.quizzes.filters import QuizFilter
from apps.quizzes.serializers import (
    QuizReadSerializer,
    QuizCreateSerializer,
    QuizUpdateSerializer,
)
from rest_framework import views
from rest_framework import generics
from apps.quizzes.models import Quiz
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count


# Create your views here.


class ListAllQuizzesAPIView(generics.ListAPIView):
    serializer_class = QuizReadSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = QuizFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "user__username"]
    # search_fields = ["=title", "user__username"] # "=" is for exact match from the search
    ordering_fields = [
        "created_at",
        "-created_at",
        "-likes_count",
    ]  # "-" is for des order
    ordering = ["-created_at"]#default ordering

    def get_queryset(self):
        return Quiz.objects.annotate(
            likes_count=Count("likes")
        )  # adding likes_count to each Quiz instance in the queryset


# api view to list quizzes of the authenticated user
class ListQuizzesAPIView(generics.ListAPIView):
    serializer_class = QuizReadSerializer
    permission_classes = [IsAuthenticated]
    # filterset_fields = ("title","category")

    def get_queryset(self):
        user = self.request.user
        quizzes = Quiz.objects.filter(user=user)
        return quizzes


class CreateQuizAPIView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Allows file uploads

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the quiz instance
        quiz = serializer.save(user=self.request.user, image=request.FILES.get("image"))
        return Response(QuizReadSerializer(quiz).data, status=status.HTTP_201_CREATED)


# Retrieve, update, or delete a specific quiz
class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT"]:
            return QuizUpdateSerializer
        return QuizReadSerializer

    def get_queryset(self):
        return Quiz.objects.filter(
            user=self.request.user
        )  # ensure that a user can only retrieve, update, or delete their own quizzes

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()  # Get the quiz instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # Save the updates

        # **Return updated data with questions included**
        return Response(QuizReadSerializer(instance).data, status=status.HTTP_200_OK)


class FollowedUsersQuizAPIView(generics.ListAPIView):
    serializer_class = QuizReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # following_users = user.following.all()
        following_users = user.following.values_list(
            "following", flat=True
        )  # .values_list("user", flat=True) → Extracts only the user IDs from the relation as a list.

        return Quiz.objects.filter(
            user__id__in=following_users
        )  # user__id tells Django to look at the id field of the user ForeignKey.
