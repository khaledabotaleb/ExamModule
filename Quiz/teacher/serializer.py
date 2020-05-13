from rest_framework import serializers
from Quiz.models import Quiz
from Question.models import Question ,TR , MCQ
from Question.serializers import QuestionSeralizer
from django.shortcuts import get_object_or_404 

class QuizSerializer(serializers.ModelSerializer):
    quiz_questions = QuestionSeralizer(many=True)
    class Meta:
        model = Quiz
        fields = [
            'quiz_id',
            'quiz_headline',
            'quiz_author',
            'quiz_real_time',
            'quiz_setion_time',
            'quiz_class_room',
            'quiz_is_launched',
            'quiz_creation_time',
            'quiz_questions',
        ]
        read_only_fields = ('quiz_id','quiz_author',)
    def addQuestionToQuiz(self , question_id, pk):
        quiz = get_object_or_404(Quiz,pk= pk)
        question = get_object_or_404(Question,question_id)
        