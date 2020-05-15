from rest_framework import serializers
from Quiz.models import Quiz
from Question.models import Question ,TR , MCQ
from Question.serializers import QuestionSeralizer
from django.shortcuts import get_object_or_404 

class QuizPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ['quiz_headline' ,'quiz_questions']



class QuizGetSerializer(serializers.ModelSerializer):
    quiz_questions = QuestionSeralizer(many = True)
    class Meta:
        model = Quiz
        fields = '__all__'

class AddQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['quiz_headline' ,]