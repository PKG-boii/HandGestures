from src.features import (
    get_thumb_direction,
    is_pinching,
    is_ok_gesture
)


class GestureClassifier:

    def classify(self, landmarks, finger_states):
        """
        Classifies a static hand gesture based on
        which fingers are extended.

        Returns:
            gesture name
        """

        thumb = finger_states["thumb"]
        index = finger_states["index"]
        middle = finger_states["middle"]
        ring = finger_states["ring"]
        pinky = finger_states["pinky"]

        # --------------------------------
        # OK
        # --------------------------------

        if is_ok_gesture(
            landmarks,
            finger_states
        ):
            return "OK"

        # --------------------------------
        # PINCH
        # --------------------------------

        if is_pinching(landmarks):

            # Avoid calling a normal OK
            # gesture simply "PINCH".
            if not (
                middle and ring and pinky
            ):
                return "PINCH"

        # --------------------------------
        # THUMBS UP / DOWN
        # --------------------------------

        if (
            thumb
            and not index
            and not middle
            and not ring
            and not pinky
        ):

            direction = get_thumb_direction(
                landmarks
            )

            if direction == "UP":
                return "THUMBS_UP"

            if direction == "DOWN":
                return "THUMBS_DOWN"

        # --------------------------------
        # FIST
        # --------------------------------

        if not thumb and not index and not middle \
                and not ring and not pinky:

            return "FIST"

        # --------------------------------
        # OPEN PALM
        # --------------------------------

        if thumb and index and middle and ring and pinky:

            return "OPEN_PALM"

        # --------------------------------
        # ROCK
        # --------------------------------

        if index and pinky and not middle and not ring:

            return "ROCK"

        # --------------------------------
        # PEACE
        # --------------------------------

        if index and middle and not ring and not pinky:

            return "PEACE"

        # --------------------------------
        # THREE
        # --------------------------------

        if index and middle and ring and not pinky:

            return "THREE"

        # --------------------------------
        # FOUR
        # --------------------------------

        if index and middle and ring and pinky and not thumb:

            return "FOUR"

        # --------------------------------
        # POINT
        # --------------------------------

        if index and not middle and not ring and not pinky:

            return "POINT"

        # --------------------------------
        # MIDDLE
        # --------------------------------

        if middle and not index and not ring and not pinky:

            return "MIDDLE"

        return "UNKNOWN"