from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QColorDialog
)


class ToolBar(QWidget):

    color_changed = Signal(QColor)
    width_changed = Signal(int)

    undo_clicked = Signal()
    redo_clicked = Signal()
    clear_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.setFixedWidth(180)

        layout = QVBoxLayout()

        title = QLabel("TOOLS")

        title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            """
        )

        layout.addWidget(title)

        # -------------------------
        # Pen
        # -------------------------

        self.pen_button = QPushButton("✏ Pen")

        layout.addWidget(
            self.pen_button
        )

        # -------------------------
        # Brush
        # -------------------------

        self.brush_button = QPushButton(
            "🖌 Brush"
        )

        layout.addWidget(
            self.brush_button
        )

        # -------------------------
        # Color
        # -------------------------

        color_label = QLabel("COLOR")

        layout.addWidget(
            color_label
        )

        self.color_button = QPushButton(
            "Choose Color"
        )

        self.color_button.clicked.connect(
            self.choose_color
        )

        layout.addWidget(
            self.color_button
        )

        # -------------------------
        # Width
        # -------------------------

        size_label = QLabel(
            "BRUSH SIZE"
        )

        layout.addWidget(
            size_label
        )

        self.size_slider = QSlider()

        self.size_slider.setOrientation(
            Qt.Orientation.Horizontal
        )

        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(50)
        self.size_slider.setValue(8)

        self.size_slider.valueChanged.connect(
            self.width_changed.emit
        )

        layout.addWidget(
            self.size_slider
        )

        # -------------------------
        # Undo
        # -------------------------

        undo_button = QPushButton(
            "↶ Undo"
        )

        undo_button.clicked.connect(
            self.undo_clicked.emit
        )

        layout.addWidget(
            undo_button
        )

        # -------------------------
        # Redo
        # -------------------------

        redo_button = QPushButton(
            "↷ Redo"
        )

        redo_button.clicked.connect(
            self.redo_clicked.emit
        )

        layout.addWidget(
            redo_button
        )

        # -------------------------
        # Clear
        # -------------------------

        clear_button = QPushButton(
            "⌫ Clear"
        )

        clear_button.clicked.connect(
            self.clear_clicked.emit
        )

        layout.addWidget(
            clear_button
        )

        layout.addStretch()

        self.setLayout(layout)

    def choose_color(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.color_changed.emit(
                color
            )
