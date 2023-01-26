from PyQt5.QtCore import *
from pipelineeditor.node_editor_widget import NodeEditorWidget


class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.scene.add_has_been_modified_listener(self.setTitle)
        self._close_event_listeners = []
        self.setTitle()

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendltFilename())

    def closeEvent(self, event) -> None:
        for callback in self._close_event_listeners:
            callback(self, event)

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)