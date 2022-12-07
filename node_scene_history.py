class SceneHistory():
    def __init__(self, scene) -> None:
        self.scene = scene
        self.history_stack = []
        self.current_step = -1
        self.history_limit = 8

    def undo(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.restore_history()

    def redo(self):
        if self.current_step + 1 < len(self.history_stack):
            self.current_step += 1
            self.restore_history()

    def restore_history(self):
        print(f"restore history current_step: {self.current_step}, stack length: {len(self.history_stack)}")
        self.restore_history_stamp(self.history_stack[self.current_step])

    def store_history(self, desc):
        print(f"store history current_step: {self.current_step}, stack length: {len(self.history_stack)}")

        if self.current_step + 1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.current_step + 1]

        if self.current_step + 1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.current_step -= 1

        hs = self.create_history_stamp(desc)

        self.history_stack.append(hs)
        self.current_step += 1

    def restore_history_stamp(self, history_stamp):
        print(f"restore_history_stamp {history_stamp}")

    def create_history_stamp(self, desc):
        return desc