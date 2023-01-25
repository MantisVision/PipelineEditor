from pipelineeditor.graphics.node_graphics_edge import QDMGraphicsEdge
from pipelineeditor.utils import dump_exception


class SceneHistory():
    def __init__(self, scene) -> None:
        self.scene = scene
        self.clear()
        self.history_limit = 32

    def clear(self):
        self.history_stack = []
        self.current_step = -1

    def store_initial_history_stamp(self):
        self.store_history("Inital history stamp")

    def can_undo(self):
        return self.current_step > 0

    def can_redo(self):
        return self.current_step + 1 < len(self.history_stack)

    def undo(self):
        if self.can_undo():
            self.current_step -= 1
            self.restore_history()

    def redo(self):
        if self.can_redo():
            self.current_step += 1
            self.restore_history()

    def restore_history(self):
        self.restore_history_stamp(self.history_stack[self.current_step])

    def store_history(self, desc, set_modified=False):
        if set_modified:
            self.scene.has_been_modified = True

        if self.current_step + 1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.current_step + 1]

        if self.current_step + 1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.current_step -= 1

        hs = self.create_history_stamp(desc)

        self.history_stack.append(hs)
        self.current_step += 1

        # print("Storing history", '"%s"' % desc,
        #     ".... current_step: @%d" % self.current_step,
        #     "(%d)" % len(self.history_stack))

    def create_history_stamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges': []
        }

        for item in self.scene.gr_scene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif item is isinstance(item, QDMGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj
        }

        return history_stamp

    def restore_history_stamp(self, history_stamp):
        self.scene.deserialize(history_stamp['snapshot'])

        try:
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.gr_edge.setSelected(True)
                        break

            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.gr_node.setSelected(True)
                        break
        except Exception as e:
            dump_exception(e)