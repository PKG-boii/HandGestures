class DrawingDocument:

    def __init__(self):

        self.objects = []

        self.redo_stack = []

    def add(self, obj):

        self.objects.append(obj)

        self.redo_stack.clear()

    def undo(self):

        if not self.objects:
            return

        obj = self.objects.pop()

        self.redo_stack.append(
            obj
        )

    def redo(self):

        if not self.redo_stack:
            return

        obj = self.redo_stack.pop()

        self.objects.append(
            obj
        )

    def clear(self):

        self.objects.clear()

        self.redo_stack.clear()

    def render(self, frame):

        for obj in self.objects:

            obj.draw(frame)

    def can_undo(self):

        return len(self.objects) > 0

    def can_redo(self):

        return len(self.redo_stack) > 0
