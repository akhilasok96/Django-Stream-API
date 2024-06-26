from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add_exercise/", views.add_exercise, name="add_exercise"),
    path("api/exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path(
        "api/exercises/id/<int:exercise_id>/",
        views.ExerciseByIdView.as_view(),
        name="exercise-by-id",
    ),
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
    path(
        "api/exercises/category/<str:category>/",
        views.ExercisesByCategoryView.as_view(),
        name="exercises-by-category",
    ),
    path("api/user/<str:email>/", views.UserDataView.as_view(), name="user-data"),
    path(
        "api/workout_logs/<str:email>/",
        views.WorkoutLogView.as_view(),
        name="workout-logs",
    ),
]
