from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('questions', views.QuestionViewSet)


app_name = 'question'

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<question_id>/reviews', views.ReviewList.as_view(),name='review-list'),
    path('questions/<question_id>/reviews/<rate_id>/',views.ReviewDetail.as_view(),name='review-detail'),
]
