from apps.attempts.models import QuizAttempt
from rest_framework import serializers

        
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'
        

class QuizAttemptSerializer(serializers.ModelSerializer):
    responses = UserResponseSerializer(many=True, read_only=True)  # Nested responses
    class Meta:
        model = QuizAttempt
        fields = '__all__'