class HistoryManager:

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, action):
        """
        Add a completed drawing action.
        """

        self.undo_stack.append(action)

        # Once a new action is made,
        # redo history is no longer valid.
        self.redo_stack.clear()

    def undo(self):

        if not self.undo_stack:
            return None

        action = self.undo_stack.pop()

        self.redo_stack.append(action)

        return action

    def redo(self):

        if not self.redo_stack:
            return None

        action = self.redo_stack.pop()

        self.undo_stack.append(action)

        return action

    def clear(self):

        self.undo_stack.clear()
        self.redo_stack.clear()

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0
