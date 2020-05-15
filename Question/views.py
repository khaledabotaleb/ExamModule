import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action , api_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from User.models import Subject, Teacher
from rest_framework import generics
from .models import MCQ, TR, Question ,Rate
from .serializers import MCQSerializer, QuestionSeralizer, TRSerializer , RateSerializer

# Custom Permissions

#  #############################################################################
# function here to add question

#  #############################################################################
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

class custom_per(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        
        t = Teacher.objects.filter(user=u).exists()   
        questions = Question.objects.get(question_author=t) 
        if t :
            if request.method in permissions.SAFE_METHODS and obj.author != t :
                return False
            else:
                return True
        else:
            return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You are not the Review auther.'
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.teacher

class QuestionViewSet(viewsets.ModelViewSet):
    """Manage Question API"""
    serializer_class = QuestionSeralizer
    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    # def get_queryset(self):
    #     """retrive the Questions for the authenticated teacher"""
    #     if hasattr(self.request.user, 'teacher'):
    #         return self.queryset.filter(question_author=self.request.user.teacher)
    #     else :
    #         return self.queryset

    def get_serializer_class(self):
        """override serializer for answer url"""
        if self.action == 'set_answer':
            question_type = self.get_object().question_type
            if question_type == 'MCQ' :
                return MCQSerializer
            elif question_type == 'TR' :
                return TRSerializer
        elif self.action == 'add_review':
            return RateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new question"""
        teacher = Teacher.objects.get(user=self.request.user)
        question_subject = teacher.subject
        serializer.save(question_author=teacher,question_subject=question_subject)

    
    @action(methods=['POST','PUT','PATCH','GET'], detail=True, url_path='set-type')
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

    # @action(methods=['POST','PUT','PATCH',], detail=True, url_path='add_review')
    # def add_review(self, request, pk=None):
    #         """Upload Image to recipe"""
    #         review = self.get_object()
    #         serializer = self.get_serializer(
    #             review,
    #             data=request.data
    #         )
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_200_OK
    #             )
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
# class RateViewSet(viewsets.ModelViewSet):
#     """Manage Rate API"""
#     serializer_class = RateSerializer
#     queryset = Rate.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly,IsAuther)

    

#     # def perform_create(self, serializer):
#     #     """Create a new Rate"""
#     #     teacher = Teacher.objects.get(user=self.request.user)
#     #     serializer.save(author=teacher)
#     @action(methods=['POST'], detail=True, url_path='add-review')
#     def add_review(self, request, pk=None):
#         """Upload Image to recipe"""
#         review = self.get_object()
#         serializer = self.get_serializer(
#             review,
#             data=request.data
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
class ReviewList(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsTeacherOrAdminOrReadOnly ,custom_per)
    lookup_url_kwarg = 'question_id'
    
    
    def perform_create(self, serializer):
            serializer.save(
                author=Teacher.objects.get(user=self.request.user),
                question_id=self.kwargs['question_id'])
    
    def get_queryset(self):
        question = self.kwargs['question_id']
        return Rate.objects.filter(question_id=question)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsTeacherOrAdminOrReadOnly,IsOwnerOrReadOnly)
    lookup_url_kwarg = 'rate_id'

    def get_queryset(self):
        review = self.kwargs['rate_id']
        return Rate.objects.filter(id=review)
#question review another solution
class ReviewApiView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsTeacherOrAdminOrReadOnly ,custom_per)
    

    def get_object(self , id):
        try:
            return Question.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        reviews = Rate.objects.filter(question_id=id)
        serializer = RateSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self,request,id):
        author = Teacher.objects.get(user=request.user)
        question = self.get_object(id)
        if question.question_author == author:
            return Response({'response': "you can not review on your question"})
        else:
            serializer = RateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    author=author,
                    question = question
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)