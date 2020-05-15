from django.urls import path , include
from Quiz.teacher.views import QuizApiViewset ,createQuiz ,QuestionList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('teacher/quizes', QuizApiViewset , basename='Quize')
urlpatterns = [
     path('',include(router.urls)),
     path('quiz/create', createQuiz , name='create'),
     path('quiz/questionlist', QuestionList , name='question_list'),
]