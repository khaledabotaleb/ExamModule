from django.urls import path , include
from Quiz.teacher import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('teacher/quizes', views.QuizViewSet)
urlpatterns = [
    path('teacher/Quizes',views.QuizesView,name='quizes' ),
]