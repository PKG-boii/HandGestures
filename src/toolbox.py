import cv2


class Toolbox:

    def __init__(self):

        self.tools = [
            "PEN",
            "BRUSH",
            "MARKER",
            "HIGHLIGHTER",
            "ERASER",
            "LINE",
            "RECTANGLE",
            "CIRCLE",
            "TRIANGLE",
            "ARROW"
        ]

        self.selected_tool = "PEN"

        self.button_size = 48
        self.spacing = 8

        self.toolbar_height = 72

        self.hovered_tool = None

    # ------------------------------------------------
    # Layout
    # ------------------------------------------------

    def calculate_layout(
        self,
        frame_width,
        frame_height
    ):

        total_width = (
            len(self.tools)
            * self.button_size
            +
            (len(self.tools) - 1)
            * self.spacing
            +
            30
        )

        x = (
            frame_width - total_width
        ) // 2

        y = (
            frame_height
            - self.toolbar_height
            - 25
        )

        return x, y

    # ------------------------------------------------
    # Button rectangle
    # ------------------------------------------------

    def get_button_rect(
        self,
        index,
        frame_width,
        frame_height
    ):

        toolbar_x, toolbar_y = (
            self.calculate_layout(
                frame_width,
                frame_height
            )
        )

        x1 = (
            toolbar_x
            + 15
            + index
            * (
                self.button_size
                + self.spacing
            )
        )

        y1 = toolbar_y + 12

        x2 = x1 + self.button_size
        y2 = y1 + self.button_size

        return (
            x1,
            y1,
            x2,
            y2
        )

    # ------------------------------------------------
    # Find tool under cursor
    # ------------------------------------------------

    def get_tool_at(
        self,
        x,
        y,
        frame_width,
        frame_height
    ):

        for i in range(len(self.tools)):

            x1, y1, x2, y2 = (
                self.get_button_rect(
                    i,
                    frame_width,
                    frame_height
                )
            )

            if (
                x1 <= x <= x2
                and
                y1 <= y <= y2
            ):

                return self.tools[i]

        return None

    # ------------------------------------------------
    # Select
    # ------------------------------------------------

    def select_tool(self, tool):

        if tool in self.tools:

            self.selected_tool = tool

    # ------------------------------------------------
    # Icons
    # ------------------------------------------------

    def get_icon(self, tool):

        icons = {

            "PEN": "P",
            "BRUSH": "B",
            "MARKER": "M",
            "HIGHLIGHTER": "H",
            "ERASER": "E",

            "LINE": "/",
            "RECTANGLE": "[]",
            "CIRCLE": "O",
            "TRIANGLE": "^",
            "ARROW": "->"
        }

        return icons.get(
            tool,
            "?"
        )

    # ------------------------------------------------
    # Draw
    # ------------------------------------------------

    def draw(
        self,
        frame,
        cursor_x=None,
        cursor_y=None
    ):

        height, width = frame.shape[:2]

        toolbar_x, toolbar_y = (
            self.calculate_layout(
                width,
                height
            )
        )

        toolbar_width = (
            len(self.tools)
            * self.button_size
            +
            (len(self.tools) - 1)
            * self.spacing
            +
            30
        )

        toolbar_y2 = (
            toolbar_y
            + self.toolbar_height
        )

        # Transparent UI layer
        overlay = frame.copy()

        # Outer panel
        cv2.rectangle(
            overlay,
            (
                toolbar_x,
                toolbar_y
            ),
            (
                toolbar_x + toolbar_width,
                toolbar_y2
            ),
            (20, 20, 20),
            -1
        )

        # Buttons
        self.hovered_tool = None

        for i, tool in enumerate(
            self.tools
        ):

            x1, y1, x2, y2 = (
                self.get_button_rect(
                    i,
                    width,
                    height
                )
            )

            hovered = False

            if cursor_x is not None:

                hovered = (
                    x1 <= cursor_x <= x2
                    and
                    y1 <= cursor_y <= y2
                )

            if hovered:

                self.hovered_tool = tool

            # Selected
            if tool == self.selected_tool:

                bg = (
                    60,
                    130,
                    80
                )

            # Hovered
            elif hovered:

                bg = (
                    80,
                    90,
                    150
                )

            else:

                bg = (
                    45,
                    45,
                    45
                )

            cv2.rectangle(
                overlay,
                (x1, y1),
                (x2, y2),
                bg,
                -1
            )

            # Border
            cv2.rectangle(
                overlay,
                (x1, y1),
                (x2, y2),
                (120, 120, 120),
                1
            )

            icon = self.get_icon(tool)

            text_size = cv2.getTextSize(
                icon,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                2
            )[0]

            text_x = (
                x1
                +
                (
                    self.button_size
                    - text_size[0]
                ) // 2
            )

            text_y = (
                y1
                +
                (
                    self.button_size
                    + text_size[1]
                ) // 2
            )

            cv2.putText(
                overlay,
                icon,
                (
                    text_x,
                    text_y
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        # Blend the entire toolbar
        cv2.addWeighted(
            overlay,
            0.60,
            frame,
            0.40,
            0,
            frame
        )

        # Tool name above toolbar
        if self.hovered_tool:

            label = self.hovered_tool

            cv2.putText(
                frame,
                label,
                (
                    toolbar_x,
                    toolbar_y - 12
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )
