import os
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(
        self,
        model_path="models/hand_landmarker.task",
        num_hands=2
    ):

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Hand landmark model not found: {model_path}"
            )

        # Configure MediaPipe
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.landmarker = vision.HandLandmarker.create_from_options(
            options
        )

    def process(self, frame, timestamp_ms):

        # OpenCV uses BGR.
        # MediaPipe expects RGB.
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert NumPy image into MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        return result

    def close(self):
        self.landmarker.close()