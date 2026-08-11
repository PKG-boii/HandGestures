import cv2


class UIOverlay:

    def draw_header(
        self,
        frame,
        fps,
        selected_tool
    ):

        overlay = frame.copy()

        # Header background
        cv2.rectangle(
            overlay,
            (20, 20),
            (280, 78),
            (20, 20, 20),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.55,
            frame,
            0.45,
            0,
            frame
        )

        # App name
        cv2.putText(
            frame,
            "AIRDRAW",
            (35, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            "Gesture Canvas",
            (36, 68),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (180, 180, 180),
            1,
            cv2.LINE_AA
        )

        # FPS
        cv2.putText(
            frame,
            f"{int(fps)} FPS",
            (
                frame.shape[1] - 100,
                45
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (220, 220, 220),
            1,
            cv2.LINE_AA
        )

        # Selected tool
        cv2.putText(
            frame,
            selected_tool,
            (
                frame.shape[1] - 130,
                65
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (160, 160, 160),
            1,
            cv2.LINE_AA
        )
