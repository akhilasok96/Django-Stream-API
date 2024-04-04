# streamapp/consumers.py
import json
import base64
import numpy as np
import cv2
import pandas as pd
from channels.generic.websocket import AsyncWebsocketConsumer
from utils import mp_pose, load_model
from type_of_exercise import TypeOfExercise
from .firebase_config import db


class VideoStreamConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.stage = None
        self.voice_prompt = ""
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.6, min_tracking_confidence=0.5
        )

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # print(data)
        exercise_type = data.get(
            "exercise_type", "bicep_curl"
        )  # Assume default exercise

        frame_data = data["data"]
        frame = base64.b64decode(frame_data.split(",")[1])
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, flags=1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            exercise_instance = TypeOfExercise(landmarks)

            if exercise_type == "bicep_curl":
                self.counter, self.stage, voice_prompt = exercise_instance.bicep_curl(
                    self.counter, self.stage
                )
            elif exercise_type == "squat":
                self.counter, self.stage, voice_prompt = exercise_instance.squat(
                    self.counter, self.stage
                )

            keypoints = [[lmk.x, lmk.y] for lmk in landmarks]
            response = {
                "keypoints": keypoints,
                "counter": self.counter,
                "stage": self.stage,
                "voice_prompt": voice_prompt,
            }
            await self.send(json.dumps(response))


class UserInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

        user_info = {
            "username": data["username"],
            "email": data["email"],
            "first_name": data["fname"],
            "last_name": data["lname"],
            "age": data["age"],
            "gender": data["gender"],
            "place": data["place"],
            "weight": data["weight"],
            "height": data["height"],
        }
        db.collection("users").add(user_info)
        await self.send(json.dumps({"status": "UserInfo saved"}))


class CaloriePredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        model_input = {
            "Gender": data.get("gender", ""),
            "Age": int(data.get("age", 0)),
            "Height": float(data.get("height", 0)),
            "Weight": float(data.get("weight", 0)),
            "Duration": float(data.get("duration", 0)),
            "Heart_Rate": float(data.get("heart_rate", 0)),
            "Body_Temp": float(data.get("body_temp", 0)),
        }

        pipeline = load_model("pipeline.pkl")

        sample = pd.DataFrame([model_input])

        prediction = pipeline.predict(sample)
        print(f"Predicted Calories Burned: {prediction[0]}")

        await self.send(json.dumps({"prediction": str(prediction[0])}))
