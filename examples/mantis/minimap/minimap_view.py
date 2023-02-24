import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from mini_node import MiniNode, MiniROI


class MinimapScene():
    def __init__(self) -> None:
        self.scene_width = 6400 // 8
        self.scene_height = 6400 // 8
        self.gr_scene = MinimapGRScene(self)
        self.gr_scene.setGrScene(self.scene_width, self.scene_height)
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)


class MinimapGRScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)


class MinimapGRView(QGraphicsView):
    def __init__(self, minimap_gr_scene, parent=None):
        super().__init__(parent)
        self.minimap_gr_scene = minimap_gr_scene
        self.setScene(self.minimap_gr_scene)
        # self.scale(0.5, 0.5)

    def mouseReleaseEvent(self, event):
        print(event.pos())

class MinimapWidget(QWidget): # noqa
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initUI()
        node = MiniNode(self.scene, "My Awesome Node1")
        roi = MiniROI(self.scene)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.scene = MinimapScene()

        # Create graphics view
        self.view = MinimapGRView(self.scene.gr_scene, self)
        self.layout.addWidget(self.view)

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')

    myApp = MinimapWidget()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')