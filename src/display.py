import cv2
import numpy as np


class DisplayManager:

    def __init__(self, window_name="AirDraw"):

        self.window_name = window_name

        cv2.namedWindow(
            self.window_name,
            cv2.WINDOW_NORMAL
        )

        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

        # OpenCV doesn't expose a reliable monitor-resolution
        # API on every platform, so we'll use the window size
        # after creation and provide a fallback.
        self.width = 1920
        self.height = 1080

    def set_size(self, width, height):

        self.width = width
        self.height = height

    def show(self, frame):

        display_frame = self._fit_frame(
            frame
        )

        cv2.imshow(
            self.window_name,
            display_frame
        )

    def _fit_frame(self, frame):

        frame_height, frame_width = frame.shape[:2]

        scale = min(
            self.width / frame_width,
            self.height / frame_height
        )

        new_width = int(
            frame_width * scale
        )

        new_height = int(
            frame_height * scale
        )

        resized = cv2.resize(
            frame,
            (
                new_width,
                new_height
            ),
            interpolation=cv2.INTER_LINEAR
        )

        # Create black display canvas
        output = np.zeros(
            (
                self.height,
                self.width,
                3
            ),
            dtype=frame.dtype
        )

        x_offset = (
            self.width - new_width
        ) // 2

        y_offset = (
            self.height - new_height
        ) // 2

        output[
            y_offset:
            y_offset + new_height,
            x_offset:
            x_offset + new_width
        ] = resized

        return output
