from apps.quizzes.models import Answer, Question, Quiz
from rest_framework import serializers

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Nested answers
    class Meta:
        model = Question
        fields = '__all__'

#todo define new quiz serializer for home page       
class QuizSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    questions = QuestionSerializer(many=True, read_only=True)  # Nested questions
    class Meta:
        model = Quiz
        fields = '__all__'
        
        
