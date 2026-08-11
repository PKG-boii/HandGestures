import cv2
import numpy as np


class DrawingLayer:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.canvas = np.zeros(
            (height, width, 4),
            dtype=np.uint8
        )

        self.is_drawing = False
        self.last_point = None

        self.color = (0, 0, 0, 255)

        self.brush_size = 8

        self.current_tool = "PEN"

    # -----------------------------------------
    # Tool
    # -----------------------------------------

    def set_tool(self, tool):

        self.current_tool = tool

    # -----------------------------------------
    # Start
    # -----------------------------------------

    def start_stroke(self, x, y):

        self.is_drawing = True

        self.last_point = (
            x,
            y
        )

    # -----------------------------------------
    # Draw
    # -----------------------------------------

    def draw(self, x, y):

        if not self.is_drawing:
            return

        if self.last_point is None:

            self.last_point = (
                x,
                y
            )

            return

        x1, y1 = self.last_point

        # -------------------------------------
        # ERASER
        # -------------------------------------

        if self.current_tool == "ERASER":

            cv2.line(
                self.canvas,
                (x1, y1),
                (x, y),
                (0, 0, 0, 0),
                self.brush_size * 2,
                cv2.LINE_AA
            )

        else:

            b, g, r, alpha = self.get_tool_style()

            cv2.line(
                self.canvas,
                (x1, y1),
                (x, y),
                (b, g, r, alpha),
                self.get_tool_width(),
                cv2.LINE_AA
            )

        self.last_point = (
            x,
            y
        )

    # -----------------------------------------
    # End
    # -----------------------------------------

    def end_stroke(self):

        self.is_drawing = False

        self.last_point = None

    # -----------------------------------------
    # Tool width
    # -----------------------------------------

    def get_tool_width(self):

        if self.current_tool == "PEN":

            return self.brush_size

        if self.current_tool == "BRUSH":

            return int(
                self.brush_size * 2
            )

        if self.current_tool == "MARKER":

            return int(
                self.brush_size * 1.5
            )

        if self.current_tool == "HIGHLIGHTER":

            return int(
                self.brush_size * 3
            )

        if self.current_tool == "ERASER":

            return self.brush_size * 2

        return self.brush_size

    # -----------------------------------------
    # Tool style
    # -----------------------------------------

    def get_tool_style(self):

        if self.current_tool == "PEN":

            return (
                self.color[0],
                self.color[1],
                self.color[2],
                255
            )

        if self.current_tool == "BRUSH":

            return (
                self.color[0],
                self.color[1],
                self.color[2],
                220
            )

        if self.current_tool == "MARKER":

            return (
                self.color[0],
                self.color[1],
                self.color[2],
                190
            )

        if self.current_tool == "HIGHLIGHTER":

            return (
                self.color[0],
                self.color[1],
                self.color[2],
                80
            )

        return (
            self.color[0],
            self.color[1],
            self.color[2],
            255
        )

    # -----------------------------------------
    # Clear
    # -----------------------------------------

    def clear(self):

        self.canvas[:] = 0

    # -----------------------------------------
    # Color
    # -----------------------------------------

    def set_color(
        self,
        b,
        g,
        r,
        a=255
    ):

        self.color = (
            b,
            g,
            r,
            a
        )

    # -----------------------------------------
    # Size
    # -----------------------------------------

    def set_brush_size(
        self,
        size
    ):

        self.brush_size = size

    # -----------------------------------------
    # Render
    # -----------------------------------------

    def render(self, frame):

        overlay = self.canvas[:, :, :3]

        alpha = (
            self.canvas[:, :, 3]
            / 255.0
        )

        alpha = alpha[:, :, np.newaxis]

        result = (
            frame * (1 - alpha)
            +
            overlay * alpha
        )

        return result.astype(
            np.uint8
        )
