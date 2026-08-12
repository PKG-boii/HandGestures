import cv2
import numpy as np


class Stroke:

    def __init__(
        self,
        points,
        color,
        width,
        tool="PEN"
    ):

        self.points = points
        self.color = color
        self.width = width
        self.tool = tool

    def draw(self, frame):

        if len(self.points) < 2:
            return

        color = self.color

        for i in range(
            1,
            len(self.points)
        ):

            p1 = self.points[i - 1]
            p2 = self.points[i]

            cv2.line(
                frame,
                p1,
                p2,
                color,
                self.width,
                cv2.LINE_AA
            )
