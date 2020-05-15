from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)

from rest_framework import permissions
from rest_framework import mixins, status, viewsets
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
import random 
from Quiz.models import Quiz
from Question.models import Question ,MCQ , TR
from User.models import Teacher , User
from Quiz.teacher.serializer import QuizPostSerializer , QuizGetSerializer , AddQuizSerializer


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
class QuizApiViewset(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly)
    queryset = Quiz.objects.all()

    # def get_queryset(self):
    #     """retrive the Quizes for the authenticated teacher"""
    #     if hasattr(self.request.user, 'teacher'):
    #         return self.queryset.filter(quiz_author=self.request.user.teacher)
    #     else :
    #         return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuizGetSerializer
        else : 
            return QuizPostSerializer
    def perform_create(self, serializer):
        """Create a new quiz"""
        teacher = Teacher.objects.get(user=self.request.user)
        subject = teacher.subject
        serializer.save(quiz_author=teacher,quiz_subject=subject)


class ArticleApiView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    # def quize_owner(self,request):
    #      user = request.user
    #     teacher= get_object_or_404(Teacher, user=user)
    #     if not teacher:
    #         return Response({'response': 'this allowed only for teacher'})
        # """retrive the Quizes for the authenticated teacher"""
        # if hasattr(self.request.user, 'teacher'):
        #     return self.queryset.filter(quiz_author=self.request.user.teacher)
        # else :
        #     return self.queryset

    def get(self , request):
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes, many=True)
        return Response(serializer.data)
    
    def post(self,request, id=None):
        quiz = quiz.objects.get(id=id)
        questions = Question
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quiz_questions=quiz_questions)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST',])
# def QuizList(request):
#     user = request.user
#     teacher= get_object_or_404(Teacher, user=user)
#      if not teacher:
#         return Response({'response': 'this allowed only for teacher'})
    
#     question_data = []
#     quiz_data =[]
#     class_room = teacher.class_rooms
@api_view(['Post'])
# @permission_classes((IsAuthenticated,))
def createQuiz(request):
    user = User.objects.get(username='khaled')
    if user:
        teacher= get_object_or_404(Teacher, user=user)
        if teacher: 
            subject = teacher.subject
            if subject: 
                if request.method == 'POST':
                    serializer = AddQuizSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(quiz_author=teacher,quiz_subject=subject)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Message' : 'there is no subjects for this teacher.'})
        else:
            return Response({'Message' : 'there is no teacher for this user.'})
    else:
        return Response({'Message' : 'there is no users.'})

@api_view(['GET',])
def QuestionList(request):
    user = User.objects.get(username='khaled')
    if user:
        teacher= get_object_or_404(Teacher, user=user)
        if teacher: 
            subject = teacher.subject
            AllQuestions = Question.objects.filter(question_subject=subject)
            questions = []
            # new_mcq = []
            for ques in AllQuestions:
                if ques.question_type =='MCQ':
                    mcq = MCQ.objects.get(question=ques)
                    questions.append(mcq.question_head)
                    questions.append(mcq.question_head_avatar)
                    questions.append(mcq.question_body)
                    questions.append(mcq.choice_A)
                    questions.append(mcq.choice_B)
                    questions.append(mcq.choice_C)
                    questions.append(mcq.choice_D)
                else:
                    tr = TR.objects.get(question=ques)
                    questions.append(tr.question_body)
            return Response(questions)
                