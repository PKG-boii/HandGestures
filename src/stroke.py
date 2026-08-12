import cv2


class Stroke:

    def __init__(
        self,
        points,
        color,
        width,
        tool="PEN"
    ):
        self.points = points
        self.color = color
        self.width = width
        self.tool = tool

    def draw(self, frame):

        if len(self.points) < 2:
            return

        width = self.width

        if self.tool == "BRUSH":
            width = int(self.width * 2)

        elif self.tool == "MARKER":
            width = int(self.width * 1.5)

        elif self.tool == "HIGHLIGHTER":
            width = int(self.width * 3)

        for i in range(1, len(self.points)):

            p1 = self.points[i - 1]
            p2 = self.points[i]

            cv2.line(
                frame,
                p1,
                p2,
                self.color,
                max(1, width),
                cv2.LINE_AA
            )
