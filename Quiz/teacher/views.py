from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)

from rest_framework import permissions
from rest_framework import mixins, status, viewsets
from django.http import HttpResponse
from rest_framework.response import Response
import random 
from Quiz.models import Quiz
from Question.models import Question ,MCQ , TR
from User.models import Teacher
from Quiz.teacher.serializer import QuizSerializer
class IsTeacherOrAdminOrReadOnly(permissions.BasePermission):
    message = 'Adding Quizes not allowed for this account.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            u = request.user
            t = Teacher.objects.filter(user=u).exists()
            if (t) : # add u.role == 'T' and 
                return True
            else:
                return False

# class QuizViewSet(viewsets.ModelViewSet):
#     """Manage Quiz API"""
#     serializer_class = QuizSerializer
#     queryset = Quiz.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    
#     def perform_create(self, serializer):
#         """Create a new question"""
#         teacher = Teacher.objects.get(user=self.request.user)
#         serializer.save(quiz_author=teacher,quiz_id = random.random()*10000)
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def QuizesView(request):
    user = request.user
    author = Teacher.objects.get(user=user)
    AllQuizes = get_object_or_404(Quiz,quiz_author=author)
    
    if request.method == 'GET':
        serializer = QuizSerializer(AllQuizes)
        return Response(serializer.data)
