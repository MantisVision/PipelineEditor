from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class QDMNodeContentWidget(QWidget):

    def __init__(self, node, parent=None) -> None:
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget_title = QLabel("Some Title")
        self.layout.addWidget(self.widget_title)
        self.layout.addWidget(QDMTextEdit("foo"))

    def setEditingFlag(self, val):
        self.node.scene.gr_scene.views()[0].editingFlag = val


class QDMTextEdit(QTextEdit):

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)