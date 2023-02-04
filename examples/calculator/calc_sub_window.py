from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path
from examples.calculator.calc_config import *
from pipelineeditor.node_editor_widget import NodeEditorWidget
from pipelineeditor.utils import dump_exception
from pipelineeditor.node_edge import EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT, EDGE_TYPE_SQUARE
from pipelineeditor.graphics.node_graphics_view import MODE_EDGE_DRAG
from examples.calculator.calc_node_base import *


class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.scene.add_has_been_modified_listener(self.setTitle)
        self.scene.history.addHistoryRestoreListener(self.onHistoryRestored)
        self.scene.add_drag_enter_listener(self.onDragEnter)
        self.scene.add_drop_listener(self.onDrop)
        self.scene.set_node_class_selector(self.getNodeClassFromData)
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
                if node.__class__.__name__ == "CalcNode_Output":
                    node.eval()
            return True
        return False

    def doEvalOutputs(self):
        for node in self.scene.nodes:
            if node.__class__.__name__ == "CalcNode_Output":
                node.eval()

    def onHistoryRestored(self):
        self.doEvalOutputs()

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendltFilename())

    def initNodesContextMenu(self):
        context_menu = QMenu(self)
        keys = list(CALC_NODES.keys())
        keys.sort()

        for key in keys:
            context_menu.addAction(self.node_actions[key])

        return context_menu

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            node = CALC_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def closeEvent(self, event) -> None:
        for callback in self._close_event_listeners:
            callback(self, event)

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def onDragEnter(self, event):
        print("Calc subwindow: onDragEnter")
        print(f"mimeData: {event.mimeData()}|")

        if event.mimeData().hasFormat(LISTBOX_MIMETYPE) or event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            print("... denided drag event")
            event.setAccepted(False)

    def onDrop(self, event):
        print("Calc subwindow: onDrop")
        print(f"mimeData: {event.mimeData().text()}|")
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
            op_code = OP_NODE_INPUT
            mouse_pos = event.pos()
            scene_pos = self.scene.getView().mapToScene(mouse_pos)

            # TODO: Fix dragging files in input files
            for i, url in enumerate(event.mimeData().urls()):
                print(f"DROP: {op_code} - {str(url)} mouse at: {mouse_pos} scene at: {scene_pos}")

                try:
                    offset = i * 20
                    node = get_class_from_op_code(OP_NODE_INPUT)(self.scene)
                    node.setPos(scene_pos.x() + offset, scene_pos.y() + offset)
                    # node.setContentTitle(Path((url.toString())).name) # Need to fix node content
                    self.scene.history.store_history(f"Created Node {node.__class__.__name__}")
                except Exception as e:
                    dump_exception(e)

            event.setDropAction(Qt.MoveAction)
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
            print(val)
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
            new_calc_node = get_class_from_op_code(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_pos.x(), scene_pos.y())

            if self.scene.getView().mode == MODE_EDGE_DRAG:
                # If we were dragging edge
                self.scene.getView().edgeDragEnd(new_calc_node.inputs[0].gr_socket)
                new_calc_node.doSelect(True)
                # new_calc_node.inputs[0].edges[-1].doSelect(True)
            else:
                self.scene.history.store_history(f"Created {new_calc_node.__class__.__name__}")
