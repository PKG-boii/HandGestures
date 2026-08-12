import cv2
import time

from src.gesture_classifier import GestureClassifier
from src.gesture_smoother import GestureSmoother
from src.dynamic_gestures import DynamicGestureDetector
from src.hand_tracker import HandTracker
from src.features import get_finger_states
from src.drawing_layer import DrawingLayer
from src.cursor import Cursor
from src.pinch_detector import PinchDetector
from src.toolbox import Toolbox
from src.color_palette import ColorPalette
from src.display import DisplayManager
from src.ui_overlay import UIOverlay
from src.shape_manager import ShapeManager
from src.shapes import Shape


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


def mouse_callback(event, x, y, flags, param):

    drawing = param

    if event == cv2.EVENT_LBUTTONDOWN:

        drawing.start_stroke(
            x,
            y
        )

    elif event == cv2.EVENT_MOUSEMOVE:

        if flags & cv2.EVENT_FLAG_LBUTTON:

            drawing.draw(
                x,
                y
            )

    elif event == cv2.EVENT_LBUTTONUP:

        drawing.end_stroke()


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

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    drawing = DrawingLayer(
        width,
        height
    )

    cursor = Cursor(
        smoothing=0.35
    )

    pinch_detector = PinchDetector()

    toolbox = Toolbox()

    palette = ColorPalette()

    ui = UIOverlay()

    shape_manager = ShapeManager()

    display = DisplayManager(
        "AirDraw"
    )

    cv2.setMouseCallback(
        display.window_name,
        mouse_callback,
        drawing
    )

    # -----------------------------
    # Create hand tracker
    # -----------------------------

    tracker = HandTracker(
        model_path="models/hand_landmarker.task",
        num_hands=2
    )

    classifier = GestureClassifier()
    smoothers = {}
    dynamic_detectors = {}

    previous_time = time.time()

    print("GestureDraw started.")
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

            cursor_x = None
            cursor_y = None
            pinching = False
            hovered_tool = None

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

                    # --------------------------------
                    # Finger states
                    # --------------------------------

                    finger_states = get_finger_states(
                        hand_landmarks
                    )

                    # --------------------------------
                    # Initialize smoothers/detectors
                    # --------------------------------

                    if hand_index not in smoothers:
                        smoothers[hand_index] = GestureSmoother(
                            history_size=7,
                            min_votes=4
                        )

                    if hand_index not in dynamic_detectors:
                        dynamic_detectors[hand_index] = DynamicGestureDetector(
                            history_size=20
                        )

                    # --------------------------------
                    # Static gesture
                    # --------------------------------

                    raw_gesture = classifier.classify(
                        hand_landmarks,
                        finger_states
                    )

                    stable_gesture = smoothers[
                        hand_index
                    ].update(
                        raw_gesture
                    )

                    # --------------------------------
                    # Dynamic gesture
                    # --------------------------------

                    dynamic_gesture = dynamic_detectors[
                        hand_index
                    ].update(
                        hand_landmarks
                    )

                    # --------------------------------
                    # Choose what to display
                    # --------------------------------

                    if dynamic_gesture is not None:

                        display_gesture = dynamic_gesture

                    else:

                        display_gesture = stable_gesture

                    # --------------------------------
                    # Draw gesture label
                    # --------------------------------

                    draw_gesture_label(
                        frame,
                        hand_landmarks,
                        display_gesture,
                        hand_index + 1
                    )

                    print(
                        f"Hand {hand_index + 1}:",
                        finger_states,
                        "→",
                        display_gesture
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

                    # --------------------------------
                    # Pinch detection
                    # --------------------------------

                    thumb_tip = hand_landmarks[4]
                    index_tip = hand_landmarks[8]

                    pinching = pinch_detector.update(
                        thumb_tip,
                        index_tip
                    )

                    # --------------------------------
                    # Cursor positioning
                    # --------------------------------

                    target_x = int(
                        index_tip.x * width
                    )

                    target_y = int(
                        index_tip.y * height
                    )

                    cursor_x, cursor_y = cursor.update(
                        target_x,
                        target_y
                    )

                    # --------------------------------
                    # Connect to drawing layer
                    # --------------------------------

                    hovered_tool = toolbox.get_tool_at(
                        cursor_x,
                        cursor_y,
                        width,
                        height
                    )

                    color_index, selected_color = palette.get_color_at(
                        cursor_x,
                        cursor_y
                    )

                    if pinching:

                        # -------------------------------
                        # Tool selection
                        # -------------------------------

                        if hovered_tool is not None:

                            toolbox.select_tool(
                                hovered_tool
                            )

                            drawing.set_tool(
                                hovered_tool
                            )

                            if drawing.is_drawing:
                                drawing.end_stroke()

                        # -------------------------------
                        # Color selection
                        # -------------------------------

                        elif color_index is not None:

                            palette.select(
                                color_index
                            )

                            b, g, r = selected_color

                            drawing.set_color(
                                b,
                                g,
                                r
                            )

                            if drawing.is_drawing:
                                drawing.end_stroke()

                        # -------------------------------
                        # Actual drawing
                        # -------------------------------

                        else:

                            # Protected UI zone - don't start drawing inside the toolbar
                            is_inside_ui = toolbox.is_inside_toolbar(
                                cursor_x,
                                cursor_y,
                                width,
                                height
                            )

                            selected_tool = toolbox.selected_tool

                            # -------------------------------
                            # Shape tool
                            # -------------------------------

                            if shape_manager.is_shape_tool(selected_tool):

                                if shape_manager.current_shape is None:

                                    if not is_inside_ui:

                                        shape_manager.start_shape(
                                            selected_tool,
                                            cursor_x,
                                            cursor_y,
                                            drawing.color[:3],
                                            drawing.brush_size
                                        )

                                else:

                                    shape_manager.update_shape(
                                        cursor_x,
                                        cursor_y
                                    )

                            # -------------------------------
                            # Freehand tool
                            # -------------------------------

                            else:

                                if not drawing.is_drawing:

                                    if not is_inside_ui:

                                        drawing.start_stroke(
                                            cursor_x,
                                            cursor_y
                                        )

                                else:

                                    drawing.draw(
                                        cursor_x,
                                        cursor_y
                                    )

                    else:

                        # Finish shape
                        if shape_manager.current_shape is not None:

                            shape_manager.finish_shape()

                        # Finish freehand stroke
                        if drawing.is_drawing:

                            drawing.end_stroke()

            else:

                cursor.reset()
                pinch_detector.reset()

                if drawing.is_drawing:
                    drawing.end_stroke()

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
                "GestureDraw | Press Q to quit",
                (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # -----------------------------
            # Composite drawing
            # -----------------------------

            frame = drawing.render(
                frame
            )

            # -----------------------------
            # Render permanent shapes
            # -----------------------------

            for shape_data in shape_manager.shapes:

                shape = Shape(
                    shape_data["type"],
                    shape_data["start"],
                    shape_data["end"],
                    shape_data["color"],
                    shape_data["width"]
                )

                shape.draw(frame)

            # -----------------------------
            # Render live shape preview
            # -----------------------------

            if shape_manager.current_shape is not None:

                current = shape_manager.current_shape

                preview = Shape(
                    current["type"],
                    current["start"],
                    current["end"],
                    current["color"],
                    current["width"]
                )

                preview.draw(
                    frame,
                    preview=True
                )

            # -----------------------------
            # Draw toolbox & color palette
            # -----------------------------

            toolbox.draw(
                frame,
                cursor_x,
                cursor_y
            )

            palette.draw(
                frame,
                cursor_x,
                cursor_y
            )

            # -----------------------------
            # Draw UI header
            # -----------------------------

            ui.draw_header(
                frame,
                fps,
                toolbox.selected_tool
            )

            # -----------------------------
            # Draw instructions
            # -----------------------------

            cv2.putText(
                frame,
                "PINCH TO SELECT / DRAW",
                (
                    frame.shape[1] - 300,
                    35
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (200, 200, 200),
                1,
                cv2.LINE_AA
            )

            # -----------------------------
            # Draw cursor
            # -----------------------------

            if cursor_x is not None and cursor_y is not None:

                cursor.draw(
                    frame,
                    cursor_x,
                    cursor_y,
                    pinching,
                    hovered_tool is not None
                )

            # -----------------------------
            # Show frame
            # -----------------------------

            display.show(frame)

            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF

            if key == ord("c"):

                drawing.clear()
                shape_manager.clear()

            elif key == ord("f"):

                display.toggle_fullscreen()

            elif key == ord("q"):

                break

    finally:

        cap.release()
        cv2.destroyAllWindows()
        tracker.close()

        print("GestureDraw stopped.")


if __name__ == "__main__":
    main()