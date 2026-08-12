class DrawingDocument:

    def __init__(self):

        self.objects = []

        self.redo_stack = []

    def add(self, obj):

        self.objects.append(obj)

        # New drawing invalidates redo history
        self.redo_stack.clear()

    def undo(self):

        if not self.objects:
            return None

        obj = self.objects.pop()

        self.redo_stack.append(obj)

        return obj

    def redo(self):

        if not self.redo_stack:
            return None

        obj = self.redo_stack.pop()

        self.objects.append(obj)

        return obj

    def clear(self):

        self.objects.clear()
        self.redo_stack.clear()

    def can_undo(self):

        return len(self.objects) > 0

    def can_redo(self):

        return len(self.redo_stack) > 0
