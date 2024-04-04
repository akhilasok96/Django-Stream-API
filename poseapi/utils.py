import mediapipe as mp
import numpy as np
from joblib import load
import os

mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def detection_body_part(landmarks, body_part_name):
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility,
    ]


def load_model(filename):
    """
    Load a machine learning model from a specified path.

    Parameters:
    - model_path: Path to the machine learning model file (e.g., .pkl file).

    Returns:
    - Loaded model.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "streamapp", filename)
    model = load(model_path)
    return model
