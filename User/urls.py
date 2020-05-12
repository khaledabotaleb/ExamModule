from django.urls import path
from . import views

urlpatterns = [
    path('register/headmaster/', views.registration_headmaster_view, name='headmasterR'),
    path('register/teacher/', views.registration_teacher_view, name='teacherR'),
    path('register/student/', views.registration_student_view, name='studentR'),
    path('register/parent/', views.registration_parent_view, name='parentR'),
]