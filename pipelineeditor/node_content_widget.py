from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from collections import OrderedDict
from pipelineeditor.serialize.node_serializable import Serializable


class QDMNodeContentWidget(QWidget, Serializable):

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
        # self._text_edit = QDMTextEdit("foo")
        # self.layout.addWidget(self._text_edit)

    def setEditingFlag(self, val):
        self.node.scene.gr_scene.views()[0].editingFlag = val

    def serialize(self):
        return OrderedDict([
            ('id', self.id)
            # ('text', self._text_edit.toPlainText())
        ])

    def deserialize(self, data, hashmap={}):
        return False

    def setTitle(self, title):
        self.widget_title.setText(title)


class QDMTextEdit(QTextEdit):

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)