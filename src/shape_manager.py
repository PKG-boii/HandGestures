class ShapeManager:

    def __init__(self):

        self.shapes = []

        self.current_shape = None

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
            return

        self.shapes.append(
            self.current_shape
        )

        self.current_shape = None

    def cancel_shape(self):

        self.current_shape = None
