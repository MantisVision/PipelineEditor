from PyQt5.QtCore import *
from pipelineeditor.node_editor_widget import NodeEditorWidget


class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.scene.add_has_been_modified_listener(self.setTitle)
        self.setTitle()

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendltFilename())