from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from .forms import ExerciseForm
from django.http import HttpResponse
import uuid
from .firebase_config import db, bucket


# Create your views here.
def home(request):
    return render(request, "base.html")


def add_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to Firebase Storage
            image = request.FILES["image"]
            blob = bucket.blob("exercise_images/{}".format(image.name))
            blob.upload_from_file(image, content_type=image.content_type)

            # Get the URL of the uploaded file
            image_url = blob.public_url

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
