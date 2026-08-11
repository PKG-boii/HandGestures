from collections import deque

from src.landmarks import WRIST


class DynamicGestureDetector:

    def __init__(
        self,
        history_size=20,
        cooldown_frames=20
    ):
        """
        Stores recent wrist positions.

        history_size:
            Number of frames kept in memory.
        """

        self.positions = deque(
            maxlen=history_size
        )

        self.cooldown_frames = cooldown_frames
        self.cooldown = 0

    def update(self, landmarks):
        """
        Add the current wrist position.

        Returns:
            dynamic gesture or None
        """

        if self.cooldown > 0:
            self.cooldown -= 1

        wrist = landmarks[WRIST]

        self.positions.append(
            (
                wrist.x,
                wrist.y
            )
        )

        if self.cooldown > 0:
            return None

        gesture = self.detect()

        if gesture is not None:

            self.cooldown = self.cooldown_frames

            self.positions.clear()

            return gesture

        return None

    def detect(self):
        """
        Detect dynamic gestures based on
        recent wrist movement.
        """

        if len(self.positions) < 8:
            return None

        positions = list(self.positions)

        x_values = [
            position[0]
            for position in positions
        ]

        y_values = [
            position[1]
            for position in positions
        ]

        # --------------------------------
        # Calculate horizontal movement
        # --------------------------------

        min_x = min(x_values)
        max_x = max(x_values)

        horizontal_range = (
            max_x - min_x
        )

        # --------------------------------
        # Calculate vertical movement
        # --------------------------------

        min_y = min(y_values)
        max_y = max(y_values)

        vertical_range = (
            max_y - min_y
        )

        # --------------------------------
        # Calculate direction changes
        # --------------------------------

        direction_changes = 0

        previous_direction = None

        for i in range(
            1,
            len(x_values)
        ):

            dx = (
                x_values[i]
                -
                x_values[i - 1]
            )

            # Ignore extremely tiny movements
            if abs(dx) < 0.015:
                continue

            current_direction = (
                1 if dx > 0 else -1
            )

            if (
                previous_direction is not None
                and
                current_direction != previous_direction
            ):

                direction_changes += 1

            previous_direction = (
                current_direction
            )

        # --------------------------------
        # SWIPE
        # --------------------------------

        start_x = x_values[0]
        end_x = x_values[-1]

        net_horizontal_movement = (
            end_x - start_x
        )

        if (
            horizontal_range > 0.25
            and
            horizontal_range > vertical_range * 1.5
        ):

            if net_horizontal_movement > 0.20:
                return "SWIPE_RIGHT"

            if net_horizontal_movement < -0.20:
                return "SWIPE_LEFT"

        # --------------------------------
        # WAVE
        # --------------------------------

        if (
            horizontal_range > 0.18
            and
            direction_changes >= 2
            and
            horizontal_range > vertical_range * 1.2
        ):

            return "WAVE"

        return None

    def reset(self):
        """
        Clear movement history.
        """

        self.positions.clear()
