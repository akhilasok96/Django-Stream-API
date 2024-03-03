from django.shortcuts import render, redirect
from .forms import ExerciseForm
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExerciseSerializer
from firebase_admin import firestore
from .firebase_config import db, bucket


def home(request):
    return render(request, "base.html")


def add_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to Firebase Storage
            image = request.FILES.get("image")  # Use .get for safer access
            if image:  # Check if an image was uploaded
                blob = bucket.blob(f"exercise_images/{image.name}")
                blob.upload_from_file(image, content_type=image.content_type)

                # Get the URL of the uploaded file
                image_url = blob.public_url
            else:
                image_url = None  # Handle case where no image is provided

            # Store exercise details in Firestore
            exercise_data = {
                "name": form.cleaned_data["name"],
                "difficulty": form.cleaned_data["difficulty"],
                "target_muscle_group": form.cleaned_data["target_muscle_group"],
                "calories_burned_per_repetition": form.cleaned_data[
                    "calories_burned_per_repetition"
                ],
                "youtube_link": form.cleaned_data["youtube_link"],
                "image_url": image_url,  # Store the URL instead of the image file
            }
            db.collection("exercises").add(exercise_data)

            return redirect("home")  # Redirect to a new URL
    else:
        form = ExerciseForm()
    return render(request, "add_exercise.html", {"form": form})


class ExerciseListView(APIView):
    def get(self, request):
        exercises = db.collection("exercises").stream()
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)


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


class ExercisesByDifficultyView(APIView):
    def get(self, request, difficulty):
        exercises = (
            db.collection("exercises").where("difficulty", "==", difficulty).stream()
        )
        exercise_list = [exercise.to_dict() for exercise in exercises]
        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data)
