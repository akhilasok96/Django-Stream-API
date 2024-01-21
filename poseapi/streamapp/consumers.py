# streamapp/consumers.py
import json
import base64
import numpy as np
import cv2
import mediapipe as mp
from channels.generic.websocket import AsyncWebsocketConsumer

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


class VideoStreamConsumer(AsyncWebsocketConsumer):
    counter = 0
    stage = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        frame_data = json.loads(text_data)["data"]
        frame = base64.b64decode(frame_data.split(",")[1])
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, flags=1)  # Convert to a cv2 image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            ]
            elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            ]
            wrist = [
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            ]
            angle = calculate_angle(shoulder, elbow, wrist)
            print(f"Calculated Angle: {angle}")

            # Bicep curl logic
            if angle > 160:
                self.stage = "down"
            if angle < 30 and self.stage == "down":
                self.stage = "up"
                self.counter += 1

            # Prepare data to send back
            keypoints = {
                f"point_{i}": [lmk.x, lmk.y] for i, lmk in enumerate(landmarks)
            }
            data = {
                "keypoints": keypoints,
                "counter": self.counter,
                "stage": self.stage,
            }
            await self.send(json.dumps(data))
