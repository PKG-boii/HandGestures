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
from src.drawing_document import DrawingDocument
from src.stroke import Stroke
from src.two_hand_manager import TwoHandManager


SHAPE_TOOLS = {
    "LINE",
    "RECTANGLE",
    "CIRCLE",
    "TRIANGLE",
    "ARROW"
}


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

    document = DrawingDocument()

    cursor = Cursor(
        smoothing=0.35
    )

    cursors = {}

    pinch_detectors = {}

    two_hand_manager = TwoHandManager()

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
            hands_data = []

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

            # ============================================================
            # HAND DETECTION
            # ============================================================

            hands = []

            if result.hand_landmarks:

                for hand_index, hand_landmarks in enumerate(
                    result.hand_landmarks
                ):

                    # ----------------------------------------------------
                    # LANDMARKS
                    # ----------------------------------------------------

                    thumb_tip = hand_landmarks[4]

                    index_tip = hand_landmarks[8]

                    # ----------------------------------------------------
                    # INDEX FINGERTIP → CAMERA COORDINATES
                    # ----------------------------------------------------

                    raw_x = int(
                        index_tip.x * width
                    )

                    raw_y = int(
                        index_tip.y * height
                    )

                    # ----------------------------------------------------
                    # PINCH
                    # ----------------------------------------------------

                    if hand_index not in pinch_detectors:

                        pinch_detectors[
                            hand_index
                        ] = PinchDetector()

                    pinching = pinch_detectors[
                        hand_index
                    ].update(
                        thumb_tip,
                        index_tip
                    )

                    # ----------------------------------------------------
                    # STORE HAND
                    # ----------------------------------------------------

                    hands.append({

                        "x": raw_x,

                        "y": raw_y,

                        "pinching": pinching,

                        "index_tip": index_tip,

                        "thumb_tip": thumb_tip

                    })

            # ============================================================
            # SORT HANDS FROM LEFT → RIGHT
            # ============================================================

            hands.sort(
                key=lambda hand: hand["x"]
            )

            # ============================================================
            # NORMAL CURSOR
            # ============================================================

            cursor_x = None
            cursor_y = None

            if len(hands) > 0:

                primary_hand = hands[0]

                cursor_x, cursor_y = cursor.update(
                    primary_hand["x"],
                    primary_hand["y"]
                )

            # ============================================================
            # TWO-HAND SHAPE MODE
            # ============================================================

            two_hand_active = False

            if len(hands) >= 2:

                hand_a = hands[0]
                hand_b = hands[1]

                both_pinching = (
                    hand_a["pinching"]
                    and
                    hand_b["pinching"]
                )

                if both_pinching:

                    two_hand_active = True

                    two_hand_manager.update(
                        hand_a,
                        hand_b
                    )

                    selected_tool = (
                        toolbox.selected_tool
                    )

                    # -----------------------------------------------
                    # Only shape tools use two-hand interaction
                    # -----------------------------------------------

                    if selected_tool in SHAPE_TOOLS:

                        point_a, point_b = (
                            two_hand_manager.get_points()
                        )

                        two_hand_preview = Shape(
                            selected_tool,
                            point_a,
                            point_b,
                            drawing.color[:3],
                            drawing.brush_size
                        )

                        two_hand_preview.draw(
                            frame,
                            preview=True
                        )

            # ============================================================
            # TWO-HAND SHAPE RELEASE
            # ============================================================

            if (
                two_hand_manager.previous_active
                and
                not two_hand_active
            ):

                point_a, point_b = (
                    two_hand_manager.get_points()
                )

                if (
                    point_a is not None
                    and
                    point_b is not None
                ):

                    selected_tool = (
                        toolbox.selected_tool
                    )

                    if selected_tool in SHAPE_TOOLS:

                        final_shape = Shape(
                            selected_tool,
                            point_a,
                            point_b,
                            drawing.color[:3],
                            drawing.brush_size
                        )

                        document.add(
                            final_shape
                        )

                two_hand_manager.reset()

            # ============================================================
            # NORMAL ONE-HAND MODE
            # ============================================================

            # Get hovered tool / color palette check for the single hand
            hovered_tool = None
            pinching = False
            if len(hands) > 0 and cursor_x is not None and cursor_y is not None:
                hovered_tool = toolbox.get_tool_at(
                    cursor_x,
                    cursor_y,
                    width,
                    height
                )

            if not two_hand_active:

                # -----------------------------------------------
                # ONE HAND EXISTS
                # -----------------------------------------------

                if len(hands) > 0:

                    primary_hand = hands[0]

                    pinching = (
                        primary_hand["pinching"]
                    )

                    # -------------------------------------------
                    # Pinching
                    # -------------------------------------------

                    if pinching:

                        color_index, selected_color = palette.get_color_at(
                            cursor_x,
                            cursor_y
                        )

                        if hovered_tool is not None:

                            toolbox.select_tool(
                                hovered_tool
                            )

                            drawing.set_tool(
                                hovered_tool
                            )

                            if drawing.is_drawing:
                                drawing.end_stroke()

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

                        else:

                            # Don't draw over toolbar
                            inside_toolbar = (
                                toolbox.is_inside_toolbar(
                                    cursor_x,
                                    cursor_y,
                                    width,
                                    height
                                )
                            )

                            if not inside_toolbar:

                                selected_tool = (
                                    toolbox.selected_tool
                                )

                                # -----------------------------------
                                # ONE-HAND SHAPE
                                # -----------------------------------

                                if selected_tool in SHAPE_TOOLS:

                                    if (
                                        shape_manager.current_shape
                                        is None
                                    ):

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

                                # -----------------------------------
                                # FREEHAND
                                # -----------------------------------

                                else:

                                    if not drawing.is_drawing:

                                        drawing.start_stroke(
                                            cursor_x,
                                            cursor_y
                                        )

                                    else:

                                        drawing.draw(
                                            cursor_x,
                                            cursor_y
                                        )

                    # -------------------------------------------
                    # RELEASE
                    # -------------------------------------------

                    else:

                        # Finish freehand stroke
                        if drawing.is_drawing:

                            if len(
                                drawing.current_points
                            ) >= 2:

                                stroke = Stroke(
                                    drawing.current_points.copy(),
                                    drawing.color[:3],
                                    drawing.brush_size,
                                    drawing.current_tool
                                )

                                document.add(
                                    stroke
                                )

                            drawing.end_stroke()

                        # Finish one-hand shape
                        if (
                            shape_manager.current_shape
                            is not None
                        ):

                            shape_data = (
                                shape_manager.finish_shape()
                            )

                            if shape_data is not None:

                                final_shape = Shape(
                                    shape_data["type"],
                                    shape_data["start"],
                                    shape_data["end"],
                                    shape_data["color"],
                                    shape_data["width"]
                                )

                                document.add(
                                    final_shape
                                )

                else:
                    for hand_id in list(cursors.keys()):
                        cursors[hand_id].reset()

                    for hand_id in list(pinch_detectors.keys()):
                        pinch_detectors[hand_id].reset()

                    if shape_manager.current_shape is not None:

                        shape_data = shape_manager.finish_shape()

                        if shape_data is not None:

                            shape = Shape(
                                shape_data["type"],
                                shape_data["start"],
                                shape_data["end"],
                                shape_data["color"],
                                shape_data["width"]
                            )

                            document.add(shape)

                    if drawing.is_drawing:

                        if len(drawing.current_points) >= 2:

                            stroke = Stroke(
                                drawing.current_points.copy(),
                                drawing.color[:3],
                                drawing.brush_size,
                                drawing.current_tool
                            )

                            document.add(stroke)

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
            # Composite drawing (Bypassed in favor of vector document rendering)
            # -----------------------------

            # frame = drawing.render(
            #     frame
            # )

            # ============================================================
            # RENDER PERMANENT DRAWING OBJECTS
            # ============================================================

            document.render(
                frame
            )

            # ============================================================
            # CURRENT FREEHAND PREVIEW
            # ============================================================

            if drawing.is_drawing:

                preview_stroke = Stroke(
                    drawing.current_points,
                    drawing.color[:3],
                    drawing.brush_size,
                    drawing.current_tool
                )

                preview_stroke.draw(
                    frame
                )

            # ============================================================
            # CURRENT ONE-HAND SHAPE PREVIEW
            # ============================================================

            if (
                shape_manager.current_shape
                is not None
            ):

                current = (
                    shape_manager.current_shape
                )

                preview_shape = Shape(
                    current["type"],
                    current["start"],
                    current["end"],
                    current["color"],
                    current["width"]
                )

                preview_shape.draw(
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

            # ============================================================
            # DRAW FINGERTIP CURSORS
            # ============================================================

            for hand in hands:

                x = hand["x"]
                y = hand["y"]

                if hand["pinching"]:

                    cv2.circle(
                        frame,
                        (x, y),
                        10,
                        (0, 255, 255),
                        -1
                    )

                    cv2.circle(
                        frame,
                        (x, y),
                        17,
                        (0, 255, 255),
                        2
                    )

                else:

                    cv2.circle(
                        frame,
                        (x, y),
                        9,
                        (255, 255, 255),
                        2
                    )

                    cv2.circle(
                        frame,
                        (x, y),
                        3,
                        (255, 255, 255),
                        -1
                    )

            if two_hand_active:

                cv2.putText(
                    frame,
                    "TWO-HAND SHAPE",
                    (
                        width - 250,
                        90
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )

            # -----------------------------
            # Show frame
            # -----------------------------

            display.show(frame)

            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF

            if key == ord("z"):

                document.undo()

            elif key == ord("y"):

                document.redo()

            elif key == ord("c"):

                drawing.clear()
                shape_manager.clear()
                document.clear()

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