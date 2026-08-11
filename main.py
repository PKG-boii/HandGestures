import cv2
import time

from src.gesture_classifier import GestureClassifier
from src.hand_tracker import HandTracker
from src.features import get_finger_states


def draw_gesture_label(frame, landmarks, gesture, hand_number):
    """
    Draws a gesture label above the detected hand.
    """

    height, width, _ = frame.shape

    # Get all x/y coordinates
    x_coords = [
        int(landmark.x * width)
        for landmark in landmarks
    ]

    y_coords = [
        int(landmark.y * height)
        for landmark in landmarks
    ]

    # Bounding box of the hand
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    # Add some padding
    padding = 10

    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)

    max_x = min(width - 1, max_x + padding)
    max_y = min(height - 1, max_y + padding)

    # Draw bounding box
    cv2.rectangle(
        frame,
        (min_x, min_y),
        (max_x, max_y),
        (255, 255, 255),
        2
    )

    # Label position
    label_x = min_x
    label_y = min_y - 10

    # If label would go outside the screen,
    # put it inside the bounding box instead.
    if label_y < 30:
        label_y = min_y + 30

    text = f"Hand {hand_number}: {gesture}"

    cv2.putText(
        frame,
        text,
        (label_x, label_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


def main():

    # -----------------------------
    # Open webcam
    # -----------------------------

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    # Optional camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # -----------------------------
    # Create hand tracker
    # -----------------------------

    tracker = HandTracker(
        model_path="models/hand_landmarker.task",
        num_hands=2
    )

    classifier = GestureClassifier()

    previous_time = time.time()

    print("GestureFlow started.")
    print("Press Q to quit.")

    try:

        while True:

            success, frame = cap.read()

            if not success:
                print("ERROR: Could not read frame.")
                break

            # Mirror the camera
            frame = cv2.flip(frame, 1)

            # Timestamp
            current_time = time.time()

            timestamp_ms = int(
                current_time * 1000
            )

            # -----------------------------
            # Detect hands
            # -----------------------------

            result = tracker.process(
                frame,
                timestamp_ms
            )

            # -----------------------------
            # Draw landmarks
            # -----------------------------

            if result.hand_landmarks:

                for hand_index, hand_landmarks in enumerate(
                    result.hand_landmarks
                ):

                    # -----------------------------
                    # Finger detection
                    # -----------------------------

                    finger_states = get_finger_states(
                        hand_landmarks
                    )

                    # -----------------------------
                    # Gesture classification
                    # -----------------------------

                    gesture = classifier.classify(
                        finger_states
                    )

                    # -----------------------------
                    # Draw gesture label
                    # -----------------------------

                    draw_gesture_label(
                        frame,
                        hand_landmarks,
                        gesture,
                        hand_index + 1
                    )

                    print(
                        f"Hand {hand_index + 1}:",
                        finger_states,
                        "→",
                        gesture
                    )

                    height, width, _ = frame.shape

                    # -----------------------------
                    # Draw landmarks
                    # -----------------------------

                    for landmark in hand_landmarks:

                        x = int(
                            landmark.x * width
                        )

                        y = int(
                            landmark.y * height
                        )

                        cv2.circle(
                            frame,
                            (x, y),
                            5,
                            (0, 255, 0),
                            -1
                        )

                    # Draw connections
                    connections = [
                        (0, 1),
                        (1, 2),
                        (2, 3),
                        (3, 4),

                        (0, 5),
                        (5, 6),
                        (6, 7),
                        (7, 8),

                        (0, 9),
                        (9, 10),
                        (10, 11),
                        (11, 12),

                        (0, 13),
                        (13, 14),
                        (14, 15),
                        (15, 16),

                        (0, 17),
                        (17, 18),
                        (18, 19),
                        (19, 20),

                        (5, 9),
                        (9, 13),
                        (13, 17)
                    ]

                    for start, end in connections:

                        x1 = int(
                            hand_landmarks[start].x * width
                        )

                        y1 = int(
                            hand_landmarks[start].y * height
                        )

                        x2 = int(
                            hand_landmarks[end].x * width
                        )

                        y2 = int(
                            hand_landmarks[end].y * height
                        )

                        cv2.line(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

            # -----------------------------
            # Calculate FPS
            # -----------------------------

            current_time = time.time()

            fps = 1 / (
                current_time - previous_time
            )

            previous_time = current_time

            # -----------------------------
            # UI
            # -----------------------------

            hand_count = len(
                result.hand_landmarks
            )

            cv2.putText(
                frame,
                f"Hands: {hand_count}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "GestureFlow | Press Q to quit",
                (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # -----------------------------
            # Show frame
            # -----------------------------

            cv2.imshow(
                "GestureFlow",
                frame
            )

            # Quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()
        tracker.close()

        print("GestureFlow stopped.")


if __name__ == "__main__":
    main()