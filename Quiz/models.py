from django.db import models
from Question.models import Question, MCQ, TR
from User.models import Teacher, ClassRoom, Student , Subject
from Report.models import ReportStudent, ReportStudentHeadMaster

class Quiz(models.Model):
    #quiz_id = models.IntegerField()
    quiz_headline = models.CharField(max_length=100, null=True, blank=True)
    quiz_questions = models.ManyToManyField(Question , related_name='quiz_questions' , blank=True)
    quiz_author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    quiz_creation_time = models.DateTimeField(auto_now_add=True)
    quiz_real_time = models.IntegerField(null=True)
    quiz_setion_time = models.IntegerField(null=True)
    quiz_is_launched = models.BooleanField(default=False)
    quiz_class_room = models.ManyToManyField(ClassRoom)
    quiz_subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)



class Answers(models.Model):
    amswers_author = models.ForeignKey(Student, on_delete=models.CASCADE)
    answers_points = models.IntegerField()
    answer = models.CharField(max_length=100, blank=True, null=True)
    time_to_answer = models.IntegerField()
    answers_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers_questions = models.ManyToManyField(Question)
    answer_report = models.ForeignKey(ReportStudent, on_delete=models.CASCADE)
    answer_report_headmaster = models.ForeignKey(ReportStudentHeadMaster, on_delete=models.CASCADE)
