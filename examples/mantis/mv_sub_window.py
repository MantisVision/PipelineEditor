from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from pipelineeditor.utils import dump_exception
from pipelineeditor.node_editor_widget import NodeEditorWidget
from pipelineeditor.graphics.node_graphics_view import MODE_EDGE_DRAG
from pipelineeditor.node_edge import EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT, EDGE_TYPE_SQUARE


class MVSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.scene.add_has_been_modified_listener(self.setTitle)
        self.scene.history.addHistoryRestoreListener(self.onHistoryRestored)
        self.scene.add_drag_enter_listener(self.onDragEnter)
        self.scene.add_drop_listener(self.onDrop)
        self.scene.set_node_class_selector(self.getNodeClassFromData)
        # self.scene.add_items_deselected_listener()
        self._close_event_listeners = []
        self.setTitle()
        self.initNewNodeActions()

    def getNodeClassFromData(self, data):
        if 'op_code' not in data:
            return Node

        return get_class_from_op_code(data['op_code'])

    def fileLoad(self, fname):
        if super().fileLoad(fname):
            for node in self.scene.nodes:
                node.eval()
            return True
        return False

    def doEvalOutputs(self):
        for node in self.scene.nodes:
            if node.__class__.__name__ == "MVNode_Output":
                node.eval()

    def onHistoryRestored(self):
        self.doEvalOutputs()

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendltFilename())

    def initNodesContextMenu(self):
        context_menu = QMenu(self)
        keys = list(MV_NODES.keys())
        keys.sort()

        for key in keys:
            context_menu.addAction(self.node_actions[key])

        return context_menu

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(MV_NODES.keys())
        keys.sort()
        for key in keys:
            node = MV_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def closeEvent(self, event) -> None:
        for callback in self._close_event_listeners:
            callback(self, event)

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def onDragEnter(self, event):
        print("MV subwindow: onDragEnter")
        print(f"mimeData: {event.mimeData()}|")

        if event.mimeData().hasFormat(LISTBOX_MIMETYPE) or event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            print("... denided drag event")
            event.setAccepted(False)

    def onDrop(self, event):
        # Drop File from Nodes ListBox
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_pos = event.pos()
            scene_pos = self.scene.getView().mapToScene(mouse_pos)

            print(f"DROP: {op_code} - {text} mouse at: {mouse_pos} scene at: {scene_pos}")

            try:
                node = get_class_from_op_code(op_code)(self.scene)
                node.setPos(scene_pos.x(), scene_pos.y())
                self.scene.history.store_history(f"Created Node {node.__class__.__name__}")
            except Exception as e:
                dump_exception(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()

        # Drop File from Windows Explorer
        elif event.mimeData().hasUrls():
            op_code = OP_NODE_S_MVX_FILE
            mouse_pos = event.pos()
            scene_pos = self.scene.getView().mapToScene(mouse_pos)

            for i, url in enumerate(event.mimeData().urls()):
                print(f"DROP: {op_code} - {str(url)} mouse at: {mouse_pos} scene at: {scene_pos}")

                try:
                    if Path(url.toLocalFile()).exists() and Path(url.toLocalFile()).suffix == ".mvx":
                        offset = i * 20
                        node = get_class_from_op_code(OP_NODE_S_MVX_FILE)(self.scene)
                        node.setPos(scene_pos.x() + offset, scene_pos.y() + offset)
                        node.setInputContent(url.toLocalFile())
                        self.scene.history.store_history(f"Created Node {node.__class__.__name__}")
                    else:
                        raise ValueError("File type is not supported")
                except Exception as e:
                    dump_exception(e)

            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            print("... ignore drop event, not in requested format")
            event.ignore()

    def contextMenuEvent(self, event) -> None:
        try:
            item = self.scene.getItemAt(event.pos())

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()
            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            else:
                self.handleNewNodeContextMenu(event)
            return super().contextMenuEvent(event)
        except Exception as e:
            dump_exception(e)

    def handleNodeContextMenu(self, event):
        context_menu = QMenu(self)
        mark_dirty_act = context_menu.addAction("Mark Dirty")
        mark_dirty_desc_act = context_menu.addAction("Mark Descendants Dirty")
        mark_invalid_act = context_menu.addAction("Mark Invalid")
        umnark_invalid_act = context_menu.addAction("Unmark Invalid")
        eval_act = context_menu.addAction("Eval")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node

        if hasattr(item, 'sokcet'):
            selected = item.socket.node

        if selected and action == eval_act:
            val = selected.eval()
        elif selected and action == mark_dirty_act:
            selected.markDirty()
        elif selected and action == mark_dirty_desc_act:
            selected.markDescendantsDirty()
        elif selected and action == mark_invalid_act:
            selected.markInvalid()
        elif selected and action == umnark_invalid_act:
            selected.markInvalid(False)

    def handleEdgeContextMenu(self, event):
        context_menu = QMenu(self)
        bezier_act = context_menu.addAction("Bezier Edge")
        direct_act = context_menu.addAction("Direct Edge")
        square_act  = context_menu.addAction("Square Edge")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezier_act:
            selected.edge_type = EDGE_TYPE_BEZIER

        if selected and action == direct_act:
            selected.edge_type = EDGE_TYPE_DIRECT

        if selected and action == square_act:
            selected.edge_type = EDGE_TYPE_SQUARE

    def handleNewNodeContextMenu(self, event):
        context_menu = self.initNodesContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action:
            new_node = get_class_from_op_code(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_node.setPos(scene_pos.x(), scene_pos.y())

            if self.scene.getView().mode == MODE_EDGE_DRAG:
                # If we were dragging edge
                target_socket = self.determine_target_socket_of_node(self.scene.getView().drag_start_socket.is_output, new_node)
                if target_socket is not None:
                    self.scene.getView().edgeDragEnd(target_socket.gr_socket)
                    self.finish_new_node_state(new_node)

            else:
                self.scene.history.store_history(f"Created {new_node.__class__.__name__}")

    def determine_target_socket_of_node(self, was_dragged_flag, new_node):
        target_socket = None
        if was_dragged_flag:
            if len(new_node.inputs) > 0:
                target_socket = new_node.inputs[0]
        else:
            if len(new_node.outputs) > 0:
                target_socket = new_node.outputs[0]
        return target_socket

    def finish_new_node_state(self, new_node):
        self.scene.doDeselectItems()
        new_node.gr_node.doSelect(True)
        new_node.gr_node.onSelected()