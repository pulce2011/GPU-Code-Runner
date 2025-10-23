from django.urls import path
from .views import ExerciseListView, RunExerciseView, CourseListView, RegisterView, UserInfoView, TaskDetailView, TaskListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('run/', RunExerciseView.as_view(), name='run-exercise'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
]

