from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QLabel
)

from .canvas_widget import CanvasWidget
from .toolbar import ToolBar


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "GestureDraw"
        )

        self.resize(
            1200,
            800
        )

        # --------------------------------
        # Central widget
        # --------------------------------

        central = QWidget()

        layout = QHBoxLayout(
            central
        )

        # --------------------------------
        # Toolbar
        # --------------------------------

        self.toolbar = ToolBar()

        layout.addWidget(
            self.toolbar
        )

        # --------------------------------
        # Canvas
        # --------------------------------

        self.canvas = CanvasWidget()

        layout.addWidget(
            self.canvas,
            1
        )

        self.setCentralWidget(
            central
        )

        # --------------------------------
        # Connect toolbar
        # --------------------------------

        self.toolbar.color_changed.connect(
            self.canvas.set_color
        )

        self.toolbar.width_changed.connect(
            self.canvas.set_width
        )

        self.toolbar.undo_clicked.connect(
            self.canvas.undo
        )

        self.toolbar.redo_clicked.connect(
            self.canvas.redo
        )

        self.toolbar.clear_clicked.connect(
            self.canvas.clear_canvas
        )
