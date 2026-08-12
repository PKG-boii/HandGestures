class TwoHandManager:

    def __init__(self):

        self.active = False

        self.left_point = None
        self.right_point = None

        self.left_pinching = False
        self.right_pinching = False

    def reset(self):

        self.active = False

        self.left_point = None
        self.right_point = None

        self.left_pinching = False
        self.right_pinching = False

    def update(
        self,
        left_hand,
        right_hand
    ):

        self.left_pinching = (
            left_hand["pinching"]
        )

        self.right_pinching = (
            right_hand["pinching"]
        )

        if self.left_pinching:

            self.left_point = (
                left_hand["x"],
                left_hand["y"]
            )

        if self.right_pinching:

            self.right_point = (
                right_hand["x"],
                right_hand["y"]
            )

        self.active = (
            self.left_pinching
            and
            self.right_pinching
        )

        return self.active
