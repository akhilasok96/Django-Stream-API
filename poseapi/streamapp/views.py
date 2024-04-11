from django.shortcuts import render, redirect
from .forms import ExerciseForm
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExerciseSerializer
from firebase_admin import firestore
from .firebase_config import db, bucket
from django.http import JsonResponse
from .serializers import UserSerializer, WorkoutLogSerializer

import random


def home(request):
    return render(request, "base.html")


def add_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.get("image")
            if image:
                blob = bucket.blob(f"exercise_images/{image.name}")
                blob.upload_from_file(image, content_type=image.content_type)

                image_url = blob.public_url
            else:
                image_url = None

            exercise_id = random.randint(1000, 2500)

            exercise_data = {
                "exercise_id": exercise_id,
                "name": form.cleaned_data["name"],
                "type": form.cleaned_data["type"],
                "category": form.cleaned_data["category"],
                "pose_estimation": form.cleaned_data["pose_estimation"],
                "difficulty": form.cleaned_data["difficulty"],
                "target_muscle_group": form.cleaned_data["target_muscle_group"],
                "description": form.cleaned_data["description"],
                "calories_burned_per_repetition": form.cleaned_data[
                    "calories_burned_per_repetition"
                ],
                "youtube_link": form.cleaned_data["youtube_link"],
                "image_url": image_url,
            }
            db.collection("exercises").add(exercise_data)

            return redirect("home")
    else:
        form = ExerciseForm()
    return render(request, "add_exercise.html", {"form": form})


class ExerciseListView(APIView):
    def get(self, request):
        exercises = db.collection("exercises").stream()
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)


class ExerciseByIdView(APIView):
    def get(self, request, exercise_id):
        exercise_id = int(exercise_id)
        exercises_ref = db.collection("exercises")
        query_ref = exercises_ref.where("exercise_id", "==", exercise_id).limit(1)
        docs = query_ref.stream()

        exercise_data = None
        for doc in docs:
            exercise_data = doc.to_dict()
            break

        if exercise_data:
            serializer = ExerciseSerializer(exercise_data)
            return Response(serializer.data)
        else:
            return Response({"error": "Exercise not found"}, status=404)


class ExercisesByTargetMuscleGroupView(APIView):
    def get(self, request, target_muscle_group):
        exercises = (
            db.collection("exercises")
            .where("target_muscle_group", "==", target_muscle_group)
            .stream()
        )
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)


class ExercisesByCategoryView(APIView):
    def get(self, request, category):
        exercises = (
            db.collection("exercises").where("category", "==", category).stream()
        )
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)


class ExercisesByDifficultyView(APIView):
    def get(self, request, difficulty):
        exercises = (
            db.collection("exercises").where("difficulty", "==", difficulty).stream()
        )
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)


class UserDataView(APIView):
    def get(self, request, email):
        users_ref = db.collection("users")
        query_ref = users_ref.where("email", "==", email).limit(1)
        docs = query_ref.stream()
        user_data = None
        for doc in docs:
            user_data = doc.to_dict()
            break

        if user_data:
            serializer = UserSerializer(user_data)
            return Response(serializer.data)
        else:
            return Response({"error": "User not found"}, status=404)


class WorkoutLogView(APIView):
    def get(self, request, email):
        workout_logs_ref = db.collection("workout_logs")
        query_ref = workout_logs_ref.where("email", "==", email).stream()

        workout_logs = [log.to_dict() for log in query_ref]

        if workout_logs:
            serializer = WorkoutLogSerializer(workout_logs, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "No workout logs found for this user"}, status=404
            )
