class TwoHandManager:

    def __init__(self):
        self.active = False

        self.point_a = None
        self.point_b = None

        self.previous_active = False

    def update(self, hand_a, hand_b):

        self.previous_active = self.active

        self.point_a = (
            hand_a["x"],
            hand_a["y"]
        )

        self.point_b = (
            hand_b["x"],
            hand_b["y"]
        )

        self.active = (
            hand_a["pinching"]
            and hand_b["pinching"]
        )

        return self.active

    def get_points(self):

        return self.point_a, self.point_b

    def just_started(self):

        return (
            self.active
            and
            not self.previous_active
        )

    def just_finished(self):

        return (
            not self.active
            and
            self.previous_active
        )

    def reset(self):

        self.active = False
        self.previous_active = False

        self.point_a = None
        self.point_b = None
