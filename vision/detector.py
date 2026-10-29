import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

import config


class HandDetector:
    def __init__(self):
        options = vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=config.MODEL_PATH),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        height, width = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.landmarker.detect_for_video(image, time.monotonic_ns() // 1_000_000)
        return [
            [(int(p.x * width), int(p.y * height)) for p in hand] for hand in result.hand_landmarks
        ]

    def close(self):
        self.landmarker.close()