from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from .objects import Stroke
from .history import HistoryManager


class DrawingCanvas(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)

        self.setStyleSheet(
            "background-color: white;"
        )

        # All completed drawing objects
        self.objects = []

        # Currently active stroke
        self.current_stroke = None

        # Drawing settings
        self.current_color = (0, 0, 0)
        self.current_width = 8

        self.is_drawing = False

        self.history = HistoryManager()

        self.setMouseTracking(True)

    # -----------------------------------------
    # Mouse press
    # -----------------------------------------

    def mousePressEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        position = event.position()

        self.current_stroke = Stroke(
            points=[
                (
                    position.x(),
                    position.y()
                )
            ],
            color=self.current_color,
            width=self.current_width
        )

        self.is_drawing = True

        self.update()

    # -----------------------------------------
    # Mouse movement
    # -----------------------------------------

    def mouseMoveEvent(self, event):

        if not self.is_drawing:
            return

        position = event.position()

        self.current_stroke.points.append(
            (
                position.x(),
                position.y()
            )
        )

        self.update()

    # -----------------------------------------
    # Mouse release
    # -----------------------------------------

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        if self.current_stroke is None:
            return

        if len(self.current_stroke.points) > 1:

            self.objects.append(
                self.current_stroke
            )

            self.history.execute(
                self.current_stroke
            )

        self.current_stroke = None

        self.is_drawing = False

        self.update()

    # -----------------------------------------
    # Rendering
    # -----------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # White canvas
        painter.fillRect(
            self.rect(),
            QColor(255, 255, 255)
        )

        # Draw completed objects
        for stroke in self.objects:

            self.draw_stroke(
                painter,
                stroke
            )

        # Draw currently active stroke
        if self.current_stroke:

            self.draw_stroke(
                painter,
                self.current_stroke
            )

    # -----------------------------------------
    # Stroke renderer
    # -----------------------------------------

    def draw_stroke(
        self,
        painter,
        stroke
    ):

        if len(stroke.points) < 2:
            return

        color = QColor(
            stroke.color[0],
            stroke.color[1],
            stroke.color[2],
            stroke.opacity
        )

        pen = QPen(
            color,
            stroke.width
        )

        pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        pen.setJoinStyle(
            Qt.PenJoinStyle.RoundJoin
        )

        painter.setPen(pen)

        points = stroke.points

        for i in range(1, len(points)):

            x1, y1 = points[i - 1]
            x2, y2 = points[i]

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

    # -----------------------------------------
    # Undo
    # -----------------------------------------

    def undo(self):

        if not self.objects:
            return

        action = self.history.undo()

        if action in self.objects:
            self.objects.remove(action)

        self.update()

    # -----------------------------------------
    # Redo
    # -----------------------------------------

    def redo(self):

        action = self.history.redo()

        if action is None:
            return

        if action not in self.objects:
            self.objects.append(action)

        self.update()

    # -----------------------------------------
    # Clear
    # -----------------------------------------

    def clear_canvas(self):

        self.objects.clear()
        self.current_stroke = None

        self.history.clear()

        self.update()

    # -----------------------------------------
    # Settings
    # -----------------------------------------

    def set_color(self, color):

        self.current_color = (
            color.red(),
            color.green(),
            color.blue()
        )

    def set_width(self, width):

        self.current_width = width
