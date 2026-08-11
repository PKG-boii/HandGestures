class GestureClassifier:

    def classify(self, finger_states):
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
        # ROCK 🤘
        # --------------------------------

        if index and pinky and not middle and not ring:

            return "ROCK"

        # --------------------------------
        # PEACE ✌️
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
        # INDEX / POINT
        # --------------------------------

        if index and not middle and not ring and not pinky:

            return "POINT"

        # --------------------------------
        # MIDDLE FINGER
        # --------------------------------

        if middle and not index and not ring and not pinky:

            return "MIDDLE"

        # --------------------------------
        # UNKNOWN
        # --------------------------------

        return "UNKNOWN"