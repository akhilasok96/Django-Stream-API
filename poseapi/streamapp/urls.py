from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add_exercise/", views.add_exercise, name="add_exercise"),
    path("api/exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path(
        "api/exercises/target/<str:target_muscle_group>/",
        views.ExercisesByTargetMuscleGroupView.as_view(),
        name="exercises-by-target-muscle-group",
    ),
    path(
        "api/exercises/difficulty/<str:difficulty>/",
        views.ExercisesByDifficultyView.as_view(),
        name="exercises-by-difficulty",
    ),
    path("api/user/<str:email>/", views.UserDataView.as_view(), name="user-data"),
]
