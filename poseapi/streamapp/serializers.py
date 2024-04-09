from rest_framework import serializers


class ExerciseSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    pose_estimation = serializers.CharField(max_length=100)
    difficulty = serializers.CharField(max_length=100, required=False)
    target_muscle_group = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    calories_burned_per_repetition = serializers.FloatField()
    youtube_link = serializers.URLField(required=False)
    image_url = serializers.URLField(required=False)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    gender = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    email = serializers.EmailField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    bmi = serializers.FloatField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    image_url = serializers.URLField()


class WorkoutLogSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    exercise_name = serializers.CharField(max_length=100)
    exercise_id = serializers.IntegerField()
    repetition = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    bmi = serializers.FloatField()
    duration = serializers.FloatField()
    predicted_calories = serializers.FloatField()
