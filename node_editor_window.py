from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.gr_scene = QDMGraphicsScene()

        # Create graphics view
        self.view = QDMGraphicsView(self.gr_scene, self)
        self.view.setScene(self.gr_scene)
        self.layout.addWidget(self.view)



        self.setWindowTitle("Pipeline Editor")
        self.show()

        self.addDebugContent()

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        
        rect = self.gr_scene.addRect(-100, -100, 100, 100, outlinePen, greenBrush)
        rect.setFlags(QGraphicsItem.ItemIsMovable)