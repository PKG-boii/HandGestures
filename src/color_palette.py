import cv2


class ColorPalette:

    def __init__(self):

        self.x = 20
        self.y = 350

        self.colors = [
            ("BLACK", (0, 0, 0)),
            ("WHITE", (255, 255, 255)),
            ("RED", (0, 0, 255)),
            ("GREEN", (0, 255, 0)),
            ("BLUE", (255, 0, 0)),
            ("YELLOW", (0, 255, 255)),
            ("PURPLE", (255, 0, 255)),
            ("ORANGE", (0, 165, 255))
        ]

        self.selected_index = 0

        self.radius = 14
        self.spacing = 38

    def get_color_at(self, x, y):

        for i, (_, color) in enumerate(
            self.colors
        ):

            cx = (
                self.x
                + 20
                + i * self.spacing
            )

            cy = self.y + 35

            distance = (
                (x - cx) ** 2
                +
                (y - cy) ** 2
            ) ** 0.5

            if distance <= self.radius:

                return i, color

        return None, None

    def select(self, index):

        if 0 <= index < len(self.colors):

            self.selected_index = index

    def draw(
        self,
        frame,
        cursor_x=None,
        cursor_y=None
    ):

        overlay = frame.copy()

        # Panel
        cv2.rectangle(
            overlay,
            (
                self.x,
                self.y
            ),
            (
                self.x + 8 * self.spacing + 35,
                self.y + 70
            ),
            (25, 25, 25),
            -1
        )

        cv2.putText(
            overlay,
            "COLORS",
            (
                self.x + 10,
                self.y + 20
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        for i, (_, color) in enumerate(
            self.colors
        ):

            cx = (
                self.x
                + 20
                + i * self.spacing
            )

            cy = self.y + 48

            selected = (
                i == self.selected_index
            )

            if selected:

                cv2.circle(
                    overlay,
                    (cx, cy),
                    self.radius + 4,
                    (255, 255, 255),
                    2
                )

            cv2.circle(
                overlay,
                (cx, cy),
                self.radius,
                color,
                -1
            )

        cv2.addWeighted(
            overlay,
            0.55,
            frame,
            0.45,
            0,
            frame
        )
