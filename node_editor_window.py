from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_node import Node
from node_scene import Scene
from node_edge import Edge

from node_graphics_view import QDMGraphicsView


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.stylesheet_file = "qss/node_style.qss"
        self.loadStylesheet(self.stylesheet_file)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.scene = Scene()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self)
        # self.view.setScene(self.gr_scene)
        self.layout.addWidget(self.view)

        self.addNodes()

        self.setWindowTitle("Pipeline Editor")
        self.show()

        # self.addDebugContent()

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.gr_scene.addRect(-100, -100, 100, 100, outlinePen, greenBrush)
        rect.setFlags(QGraphicsItem.ItemIsMovable)

    def loadStylesheet(self, filename):
        print(f"STYLE loading: {filename}")
        q_file = QFile(filename)
        q_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = q_file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))

    def addNodes(self):
        node1 = Node(self.scene, "My Awesome Node1", inputs=[1, 1, 1], outputs=[1])
        node2 = Node(self.scene, "My Awesome Node2", inputs=[1, 1, 1], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node3", inputs=[1, 1, 1], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -250)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        edge2 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=2)