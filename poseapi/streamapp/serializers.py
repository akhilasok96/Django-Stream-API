from rest_framework import serializers


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    difficulty = serializers.CharField(max_length=100, required=False)
    target_muscle_group = serializers.CharField(max_length=100)
    calories_burned_per_repetition = serializers.FloatField()
    youtube_link = serializers.URLField(required=False)
    image_url = serializers.URLField(required=False)
