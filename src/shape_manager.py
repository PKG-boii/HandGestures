class ShapeManager:

    SHAPE_TOOLS = {
        "LINE",
        "RECTANGLE",
        "CIRCLE",
        "TRIANGLE",
        "ARROW"
    }

    def __init__(self):

        self.shapes = []

        self.current_shape = None

    def is_shape_tool(self, tool):

        return tool in self.SHAPE_TOOLS

    def start_shape(
        self,
        shape_type,
        x,
        y,
        color,
        width
    ):

        self.current_shape = {
            "type": shape_type,
            "start": (x, y),
            "end": (x, y),
            "color": color,
            "width": width
        }

    def update_shape(
        self,
        x,
        y
    ):

        if self.current_shape is None:
            return

        self.current_shape["end"] = (
            x,
            y
        )

    def finish_shape(self):

        if self.current_shape is None:
            return None

        finished = self.current_shape

        self.shapes.append(
            finished
        )

        self.current_shape = None

        return finished

    def cancel_shape(self):

        self.current_shape = None

    def clear(self):

        self.shapes.clear()

        self.current_shape = None
