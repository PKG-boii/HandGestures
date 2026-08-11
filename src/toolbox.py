import cv2


class Toolbox:

    def __init__(self):

        self.x = 20
        self.y = 20

        self.width = 180
        self.button_height = 50

        self.tools = [
            "PEN",
            "BRUSH",
            "MARKER",
            "HIGHLIGHTER",
            "ERASER"
        ]

        self.selected_tool = "PEN"

    def get_button_rect(self, index):

        x1 = self.x
        y1 = (
            self.y
            + 45
            + index * self.button_height
        )

        x2 = self.x + self.width
        y2 = y1 + self.button_height

        return x1, y1, x2, y2

    def get_tool_at(self, x, y):

        for i, tool in enumerate(self.tools):

            x1, y1, x2, y2 = (
                self.get_button_rect(i)
            )

            if (
                x1 <= x <= x2
                and
                y1 <= y <= y2
            ):
                return tool

        return None

    def select_tool(self, tool):

        if tool in self.tools:
            self.selected_tool = tool

    def draw(self, frame, cursor_x=None, cursor_y=None):

        # -----------------------------------------
        # Create transparent UI layer
        # -----------------------------------------

        overlay = frame.copy()

        panel_x1 = self.x
        panel_y1 = self.y

        panel_x2 = (
            self.x
            + self.width
        )

        panel_y2 = (
            self.y
            + 45
            + len(self.tools)
            * self.button_height
        )

        # Semi-transparent panel
        cv2.rectangle(
            overlay,
            (panel_x1, panel_y1),
            (panel_x2, panel_y2),
            (25, 25, 25),
            -1
        )

        # -----------------------------------------
        # Title
        # -----------------------------------------

        cv2.putText(
            overlay,
            "TOOLS",
            (
                self.x + 15,
                self.y + 30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # -----------------------------------------
        # Buttons
        # -----------------------------------------

        for i, tool in enumerate(self.tools):

            x1, y1, x2, y2 = (
                self.get_button_rect(i)
            )

            hovered = False

            if cursor_x is not None:

                hovered = (
                    x1 <= cursor_x <= x2
                    and
                    y1 <= cursor_y <= y2
                )

            # Selected
            if tool == self.selected_tool:

                background = (
                    60,
                    130,
                    70
                )

            # Hover
            elif hovered:

                background = (
                    80,
                    90,
                    150
                )

            else:

                background = (
                    50,
                    50,
                    50
                )

            cv2.rectangle(
                overlay,
                (x1, y1),
                (x2, y2),
                background,
                -1
            )

            cv2.rectangle(
                overlay,
                (x1, y1),
                (x2, y2),
                (130, 130, 130),
                1
            )

            cv2.putText(
                overlay,
                tool,
                (
                    x1 + 15,
                    y1 + 33
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        # -----------------------------------------
        # Blend UI with camera
        # -----------------------------------------

        cv2.addWeighted(
            overlay,
            0.55,
            frame,
            0.45,
            0,
            frame
        )
