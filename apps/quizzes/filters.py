import django_filters

from apps.quizzes.models import Quiz


class QuizFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )

    class Meta:
        model = Quiz
        fields = {
            "created_at": ["exact", "range"],
            "category": ["exact", "icontains"],
            "difficulty": ["exact", "icontains"],
        }
