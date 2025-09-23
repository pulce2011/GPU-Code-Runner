from django.urls import path
from .views import ExerciseListView, RunExerciseView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('run/', RunExerciseView.as_view(), name='run-exercise'),

]

