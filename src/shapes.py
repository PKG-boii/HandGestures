import cv2
import math


class Shape:

    def __init__(
        self,
        shape_type,
        start,
        end,
        color,
        width
    ):

        self.shape_type = shape_type

        self.start = start
        self.end = end

        self.color = color
        self.width = width

    def draw(self, frame):

        x1, y1 = self.start
        x2, y2 = self.end

        if self.shape_type == "LINE":

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                self.color,
                self.width,
                cv2.LINE_AA
            )

        elif self.shape_type == "RECTANGLE":

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                self.color,
                self.width
            )

        elif self.shape_type == "CIRCLE":

            radius = int(
                math.sqrt(
                    (x2 - x1) ** 2
                    +
                    (y2 - y1) ** 2
                )
            )

            cv2.circle(
                frame,
                (x1, y1),
                radius,
                self.color,
                self.width,
                cv2.LINE_AA
            )

        elif self.shape_type == "TRIANGLE":

            self.draw_triangle(
                frame
            )

        elif self.shape_type == "ARROW":

            cv2.arrowedLine(
                frame,
                (x1, y1),
                (x2, y2),
                self.color,
                self.width,
                cv2.LINE_AA,
                tipLength=0.15
            )

    def draw_triangle(self, frame):

        x1, y1 = self.start
        x2, y2 = self.end

        left = min(x1, x2)
        right = max(x1, x2)

        top = min(y1, y2)
        bottom = max(y1, y2)

        center_x = (
            left + right
        ) // 2

        points = [
            (
                center_x,
                top
            ),
            (
                left,
                bottom
            ),
            (
                right,
                bottom
            )
        ]

        cv2.polylines(
            frame,
            [
                __import__("numpy").array(
                    points,
                    dtype="int32"
                )
            ],
            True,
            self.color,
            self.width,
            cv2.LINE_AA
        )
