from django import forms


class ExerciseForm(forms.Form):
    name = forms.CharField(label="Exercise Name", max_length=100)
    type = forms.CharField(label="Exercise Type", max_length=100)
    category = forms.CharField(label="Category", max_length=100)
    difficulty = forms.CharField(
        label="Difficulty Level", max_length=100, required=False
    )
    pose_estimation = forms.CharField(label="Pose Estimation", max_length=100)
    target_muscle_group = forms.CharField(label="Target Muscle Group", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    calories_burned_per_repetition = forms.FloatField(
        label="Calories Burned Per Repetition"
    )
    youtube_link = forms.URLField(label="YouTube Link", required=False)
    image = forms.ImageField(label="Exercise Image", required=False)
