import cv2
import numpy as np


class DrawingLayer:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # Transparent RGBA drawing layer
        self.canvas = np.zeros(
            (height, width, 4),
            dtype=np.uint8
        )

        self.is_drawing = False
        self.last_point = None

        # Default drawing settings
        self.color = (0, 0, 0, 255)
        self.brush_size = 8

    def start_stroke(self, x, y):

        self.is_drawing = True
        self.last_point = (x, y)

    def draw(self, x, y):

        if not self.is_drawing:
            return

        if self.last_point is None:
            self.last_point = (x, y)
            return

        x1, y1 = self.last_point

        # OpenCV uses BGRA here
        b, g, r, a = self.color

        cv2.line(
            self.canvas,
            (x1, y1),
            (x, y),
            (b, g, r, a),
            self.brush_size,
            cv2.LINE_AA
        )

        self.last_point = (x, y)

    def end_stroke(self):

        self.is_drawing = False
        self.last_point = None

    def clear(self):

        self.canvas[:] = 0

    def set_color(self, b, g, r, a=255):

        self.color = (b, g, r, a)

    def set_brush_size(self, size):

        self.brush_size = size

    def render(self, frame):

        # Separate RGB image and alpha channel
        overlay = self.canvas[:, :, :3]
        alpha = self.canvas[:, :, 3] / 255.0

        alpha = alpha[:, :, np.newaxis]

        # Alpha composite drawing over camera
        result = (
            frame * (1 - alpha)
            + overlay * alpha
        )

        return result.astype(np.uint8)
