import django_filters

from apps.quizzes.models import Quiz

class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ("user", "created_at", "category", "difficulty")
