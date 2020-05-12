from django.db import models
from User.models import Student, Teacher, HeadMaster


class ReportStudent(models.Model):
    report_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)

class ReportStudentHeadMaster(models.Model):
    report_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(HeadMaster, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)


class ReportTeacher(models.Model):
    report_head = models.CharField(max_length=150)
    report_body = models.CharField(max_length=500)
    report_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(HeadMaster, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)
