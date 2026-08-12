import cv2
import numpy as np
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
        self.width = max(1, int(width))

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        frame,
        preview=False
    ):

        if preview:

            # Draw preview on a separate layer
            overlay = frame.copy()

            self._draw_shape(
                overlay
            )

            cv2.addWeighted(
                overlay,
                0.65,
                frame,
                0.35,
                0,
                frame
            )

        else:

            self._draw_shape(
                frame
            )

    # =========================================================
    # ACTUAL SHAPE RENDERING
    # =========================================================

    def _draw_shape(
        self,
        frame
    ):

        x1, y1 = self.start
        x2, y2 = self.end

        # -----------------------------------------------------
        # LINE
        # -----------------------------------------------------

        if self.shape_type == "LINE":

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                self.color,
                self.width,
                cv2.LINE_AA
            )

        # -----------------------------------------------------
        # RECTANGLE
        # -----------------------------------------------------

        elif self.shape_type == "RECTANGLE":

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                self.color,
                self.width,
                cv2.LINE_AA
            )

        # -----------------------------------------------------
        # CIRCLE
        # -----------------------------------------------------

        elif self.shape_type == "CIRCLE":

            left = min(x1, x2)
            right = max(x1, x2)

            top = min(y1, y2)
            bottom = max(y1, y2)

            center_x = (
                left + right
            ) // 2

            center_y = (
                top + bottom
            ) // 2

            radius_x = (
                right - left
            ) // 2

            radius_y = (
                bottom - top
            ) // 2

            # Make it a REAL circle
            radius = min(
                radius_x,
                radius_y
            )

            if radius > 0:

                cv2.circle(
                    frame,
                    (
                        center_x,
                        center_y
                    ),
                    radius,
                    self.color,
                    self.width,
                    cv2.LINE_AA
                )

        # -----------------------------------------------------
        # TRIANGLE
        # -----------------------------------------------------

        elif self.shape_type == "TRIANGLE":

            left = min(x1, x2)
            right = max(x1, x2)

            top = min(y1, y2)
            bottom = max(y1, y2)

            center_x = (
                left + right
            ) // 2

            points = np.array(
                [
                    [
                        center_x,
                        top
                    ],
                    [
                        left,
                        bottom
                    ],
                    [
                        right,
                        bottom
                    ]
                ],
                dtype=np.int32
            )

            cv2.polylines(
                frame,
                [points],
                True,
                self.color,
                self.width,
                cv2.LINE_AA
            )

        # -----------------------------------------------------
        # ARROW
        # -----------------------------------------------------

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
