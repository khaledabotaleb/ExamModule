from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('review',views.RateViewSet)

app_name = 'question'

urlpatterns = [
    path('', include(router.urls))
]
