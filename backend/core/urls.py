from django.urls import path
from .views import ExerciseListView, RunExerciseView, CourseListView, RegisterView, UserInfoView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('run/', RunExerciseView.as_view(), name='run-exercise'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserInfoView.as_view(), name='user-info'),
]

