import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from User.models import Subject, Teacher

from .models import MCQ, TR, Question ,Rate
from .serializers import MCQSerializer, QuestionSeralizer, TRSerializer , RateSerializer

# Custom Permissions


class IsTeacherOrAdminOrReadOnly(permissions.BasePermission):
    message = 'Adding Questions not allowed for this account.'

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
class IsAuther(permissions.BasePermission):
    message = 'You are not the Review auther.'
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user.teacher
        # Check for review auther then return

class QuestionViewSet(viewsets.ModelViewSet):
    """Manage Question API"""
    serializer_class = QuestionSeralizer
    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        """retrive the Questions for the authenticated teacher"""
        if hasattr(self.request.user, 'teacher'):
            return self.queryset.filter(question_author=self.request.user.teacher)
        else :
            return self.queryset

    def get_serializer_class(self):
        """override serializer for answer url"""
        if self.action == 'set_answer':
            question_type = self.get_object().question_type
            if question_type == 'MCQ' :
                return MCQSerializer
            elif question_type == 'TR' :
                return TRSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new question"""
        teacher = Teacher.objects.get(user=self.request.user)
        serializer.save(question_author=teacher,question_id=random.random()*10000)

    @action(methods=['POST','PUT','PATCH','GET'], detail=True, url_path='set-answer')
    def set_answer(self, request, pk=None):
        """Upload Answer to question"""
        question = self.get_object()
        answer_object = question.get_answer_object()
        if answer_object :
            serializer = self.get_serializer(
                answer_object,
                data=request.data,
                partial=True,
            )
        else :
            serializer = self.get_serializer(
                data=request.data,
                partial=True,)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class RateViewSet(viewsets.ModelViewSet):
    """Manage Rate API"""
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly,IsAuther)

    

    def perform_create(self, serializer):
        """Create a new Rate"""
        teacher = Teacher.objects.get(user=self.request.user)
        serializer.save(author=teacher)