from PyQt5.QtWidgets import *

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
        self.gr_scene = QGraphicsScene()

        # Create graphics view
        self.view = QGraphicsView(self)
        self.view.setScene(self.gr_scene)
        self.layout.addWidget(self.view)



        self.setWindowTitle("Pipeline Editor")
        self.show()