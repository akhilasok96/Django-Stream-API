from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add_exercise", views.add_exercise, name="add_exercise"),
]
