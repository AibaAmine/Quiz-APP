from apps.quizzes.models import Answer, Question, Quiz
from rest_framework import serializers
from django.conf import settings  # To get Cloudinary base URL
import json


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        # extra_kwargs = {"question": {"required": False}}


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Nested answers

    class Meta:
        model = Question
        fields = "__all__"
        # extra_kwargs = {"quiz": {"required": False}}


# For POST requests (creation)
class QuizCreateSerializer(serializers.ModelSerializer):
    questions = serializers.CharField(write_only=True)  # Accepts JSON string
    user = serializers.StringRelatedField()  # Show username instead of ID
    image = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = "__all__"

    def create(self, validated_data):
        questions_json = validated_data.pop("questions", "[]") 

        print(f"Raw Questions Data: {questions_json}")  

        try:
            questions_data = json.loads(questions_json)  # Convert JSON string to list
            print(f"Parsed Questions Data: {questions_data}")  
        except json.JSONDecodeError:
            raise serializers.ValidationError({"questions": "Invalid JSON format."})

        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question_instance = Question.objects.create(quiz=quiz, **question_data)

            for answer in answers_data:
                Answer.objects.create(question=question_instance, **answer)

        return quiz

    def get_image(self, obj):
        if obj.image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/{obj.image}"
        return None


# For GET requests (read-only operations)
class QuizReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    image = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"

    def get_image(self, obj):
        if obj.image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/{obj.image}"
        return None


class QuizUpdateSerializer(serializers.ModelSerializer):
    questions = serializers.CharField(
        write_only=True, required=False
    )  # Accepts JSON for updates

    class Meta:
        model = Quiz
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}  # Make 'user' optional


    def update(self, instance, validated_data):
        questions_json = validated_data.pop("questions", None)
        validated_data.pop("user", None)  # Remove 'user' if present in request


        if questions_json:
            try:
                questions_data = json.loads(questions_json)  # Parse JSON input
            except json.JSONDecodeError:
                raise serializers.ValidationError({"questions": "Invalid JSON format."})

            # Delete old questions 
            instance.questions.all().delete()

            # Add new questions and answers
            for question_data in questions_data:
                answers_data = question_data.pop("answers", [])
                question_instance = Question.objects.create(
                    quiz=instance, **question_data
                )

                for answer in answers_data:
                    Answer.objects.create(question=question_instance, **answer)

        return super().update(instance, validated_data)
