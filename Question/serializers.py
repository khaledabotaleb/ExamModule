from rest_framework import serializers
from .models import Question, MCQ, TR , Rate

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ('id', 'question_head', 'question_body','question_head_avatar',
                  'choice_A', 'choice_B', 'choice_C', 'choice_D', 'question_answer')
        read_only_fields = ('id',)


class TRSerializer(serializers.ModelSerializer):
    class Meta:
        model = TR
        fields = ('question_body', 'question_answer')

class QuestionSeralizer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('id','question_id', 'question_author', 'question_subject', 'question_type', 'question_real_time', 'question_points',
                  'question_grade', 'question_level', 'question_educational_type', 'question_subject', 'question_topic','answer')
        read_only_fields = ('question_id','question_author')

    def get_answer(self, obj):
        if obj.question_type == 'TR' and hasattr(obj, 'tr'):
            return TRSerializer(obj.tr).data
        elif obj.question_type == 'MCQ' and hasattr(obj, 'mcq'):
            return MCQSerializer(obj.mcq).data
        else :
            return None

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('id','author','question', 'stars', 'comment','creation_time')
        read_only_fields = ('id', 'author')

    def __init__(self, *args, **kwargs):
        super(RateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        qs = Question.objects.all()
        if hasattr(request_user, 'teacher'):
            qs = qs.exclude(question_author=request_user.teacher)
        self.fields['question'].queryset = qs
        
