from collections import deque
from collections import Counter


class GestureSmoother:

    def __init__(
        self,
        history_size=7,
        min_votes=4
    ):
        """
        history_size:
            Number of recent predictions we remember.

        min_votes:
            Minimum number of votes required for
            a gesture to become stable.
        """

        self.history = deque(
            maxlen=history_size
        )

        self.min_votes = min_votes

        self.current_gesture = "UNKNOWN"

    def update(self, gesture):
        """
        Add a new prediction and return the
        currently stable gesture.
        """

        self.history.append(gesture)

        # Don't try to stabilize UNKNOWN
        # immediately.
        valid_predictions = [
            g for g in self.history
            if g != "UNKNOWN"
        ]

        if not valid_predictions:
            return self.current_gesture

        counts = Counter(
            valid_predictions
        )

        most_common_gesture, votes = (
            counts.most_common(1)[0]
        )

        if votes >= self.min_votes:

            self.current_gesture = (
                most_common_gesture
            )

        return self.current_gesture

    def reset(self):
        """
        Clears the gesture history.
        """

        self.history.clear()

        self.current_gesture = "UNKNOWN"
