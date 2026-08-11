from math import hypot


class PinchDetector:

    def __init__(
        self,
        pinch_threshold=0.06,
        release_threshold=0.09
    ):
        self.pinch_threshold = pinch_threshold
        self.release_threshold = release_threshold

        self.is_pinching = False

    def update(
        self,
        thumb_tip,
        index_tip
    ):
        dx = (
            thumb_tip.x -
            index_tip.x
        )

        dy = (
            thumb_tip.y -
            index_tip.y
        )

        distance = hypot(
            dx,
            dy
        )

        # Start pinch
        if not self.is_pinching:

            if distance < self.pinch_threshold:

                self.is_pinching = True

        # Release pinch
        else:

            if distance > self.release_threshold:

                self.is_pinching = False

        return self.is_pinching

    def reset(self):

        self.is_pinching = False
