# streamapp/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/stream/$", consumers.VideoStreamConsumer.as_asgi()),
    re_path(r"^ws/user_info/$", consumers.UserInfoConsumer.as_asgi()),
    re_path(r"^ws/calorie_prediction/$", consumers.CaloriePredictionConsumer.as_asgi()),
    re_path(r"ws/workout_logs/$", consumers.WorkoutLogsConsumer.as_asgi()),
]
