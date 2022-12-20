from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pathlib import Path
from pipelineeditor.node_node import Node
from pipelineeditor.node_scene import Scene
from pipelineeditor.node_edge import Edge

from pipelineeditor.graphics.node_graphics_view import QDMGraphicsView


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.filename = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.scene = Scene()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self)
        # self.view.setScene(self.gr_scene)
        self.layout.addWidget(self.view)

        self.add_nodes()

        self.scene.gr_scene.scene.history.store_history("Init scene")

    def isFilenameSet(self):
        return self.filename is not None

    def isModified(self):
        return self.scene.has_been_modified

    def getUserFriendltFilename(self):
        name = Path(self.filename).filename if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")


    def add_nodes(self):
        node1 = Node(self.scene, "My Awesome Node1", inputs=[0, 2, 3], outputs=[1])
        node2 = Node(self.scene, "My Awesome Node2", inputs=[1, 2, 3], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node3", inputs=[0, 2, 3], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -250)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=2)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[1], edge_type=2)