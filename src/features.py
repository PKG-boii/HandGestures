import math

from src.landmarks import (
    WRIST,

    THUMB_MCP,
    THUMB_IP,
    THUMB_TIP,

    INDEX_MCP,
    INDEX_PIP,
    INDEX_DIP,
    INDEX_TIP,

    MIDDLE_MCP,
    MIDDLE_PIP,
    MIDDLE_DIP,
    MIDDLE_TIP,

    RING_MCP,
    RING_PIP,
    RING_DIP,
    RING_TIP,

    PINKY_MCP,
    PINKY_PIP,
    PINKY_DIP,
    PINKY_TIP,
)


def distance(a, b):
    """
    Euclidean distance between two landmarks.
    """

    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )


def angle(a, b, c):
    """
    Calculates angle ABC in degrees.

    a ---- b ---- c
          ↑
        vertex
    """

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    )

    dot_product = (
        ba[0] * bc[0] +
        ba[1] * bc[1] +
        ba[2] * bc[2]
    )

    magnitude_ba = math.sqrt(
        ba[0] ** 2 +
        ba[1] ** 2 +
        ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2 +
        bc[1] ** 2 +
        bc[2] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine = dot_product / (
        magnitude_ba * magnitude_bc
    )

    # Floating-point errors can sometimes
    # produce values slightly outside [-1, 1].
    cosine = max(-1, min(1, cosine))

    return math.degrees(
        math.acos(cosine)
    )


def is_finger_extended(
    landmarks,
    mcp_index,
    pip_index,
    dip_index
):
    """
    Determines whether a finger is extended
    by measuring the angle at the PIP joint.

    Straight finger  -> angle close to 180°
    Folded finger   -> significantly smaller angle
    """

    pip_angle = angle(
        landmarks[mcp_index],
        landmarks[pip_index],
        landmarks[dip_index]
    )

    return pip_angle > 160


def is_thumb_extended(landmarks):
    """
    Determines whether the thumb is extended.

    Thumb geometry is different from the other
    fingers, so we use distances and angles.
    """

    thumb_angle = angle(
        landmarks[THUMB_MCP],
        landmarks[THUMB_IP],
        landmarks[THUMB_TIP]
    )

    return thumb_angle > 150


def get_finger_states(landmarks):

    states = {

        "thumb": is_thumb_extended(
            landmarks
        ),

        "index": is_finger_extended(
            landmarks,
            INDEX_MCP,
            INDEX_PIP,
            INDEX_DIP
        ),

        "middle": is_finger_extended(
            landmarks,
            MIDDLE_MCP,
            MIDDLE_PIP,
            MIDDLE_DIP
        ),

        "ring": is_finger_extended(
            landmarks,
            RING_MCP,
            RING_PIP,
            RING_DIP
        ),

        "pinky": is_finger_extended(
            landmarks,
            PINKY_MCP,
            PINKY_PIP,
            PINKY_DIP
        )
    }

    return states


def get_thumb_direction(landmarks):
    """
    Determines whether the thumb is pointing
    mostly upward or downward relative to the image.

    Returns:
        "UP"
        "DOWN"
        "SIDE"
    """

    thumb_tip = landmarks[THUMB_TIP]
    thumb_mcp = landmarks[THUMB_MCP]

    dy = thumb_tip.y - thumb_mcp.y

    # In image coordinates:
    # smaller y = higher on screen
    if dy < -0.12:
        return "UP"

    if dy > 0.12:
        return "DOWN"

    return "SIDE"


def is_pinching(landmarks):
    """
    Detects whether the thumb and index finger
    are close together.

    Uses palm size to normalize the distance.
    """

    thumb_tip = landmarks[THUMB_TIP]
    index_tip = landmarks[INDEX_TIP]

    wrist = landmarks[WRIST]
    middle_mcp = landmarks[MIDDLE_MCP]

    pinch_distance = distance(
        thumb_tip,
        index_tip
    )

    palm_size = distance(
        wrist,
        middle_mcp
    )

    if palm_size == 0:
        return False

    normalized_distance = (
        pinch_distance / palm_size
    )

    return normalized_distance < 0.35


def is_ok_gesture(landmarks, finger_states):
    """
    Detects the OK gesture.

    Thumb and index form a small circle,
    while the other three fingers are extended.
    """

    if not finger_states["middle"]:
        return False

    if not finger_states["ring"]:
        return False

    if not finger_states["pinky"]:
        return False

    thumb_tip = landmarks[THUMB_TIP]
    index_tip = landmarks[INDEX_TIP]

    wrist = landmarks[WRIST]
    middle_mcp = landmarks[MIDDLE_MCP]

    tip_distance = distance(
        thumb_tip,
        index_tip
    )

    palm_size = distance(
        wrist,
        middle_mcp
    )

    if palm_size == 0:
        return False

    normalized_distance = (
        tip_distance / palm_size
    )

    return normalized_distance < 0.40