class Cursor:

    def __init__(self, smoothing=0.35):

        self.x = None
        self.y = None

        self.smoothing = smoothing

    def update(self, target_x, target_y):

        # First detection
        if self.x is None or self.y is None:

            self.x = target_x
            self.y = target_y

            return int(self.x), int(self.y)

        # Exponential smoothing
        self.x = (
            self.x * (1 - self.smoothing)
            + target_x * self.smoothing
        )

        self.y = (
            self.y * (1 - self.smoothing)
            + target_y * self.smoothing
        )

        return int(self.x), int(self.y)

    def reset(self):

        self.x = None
        self.y = None
