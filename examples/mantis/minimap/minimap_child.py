import types
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from examples.mantis.mv_sub_window import MVSubWindow


class MinimapChild(MVSubWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.replaceDef()
        self.view.setAcceptDrops(False)
        self.view.setDragMode(QGraphicsView.NoDrag)

    def replaceDef(self):
        self.scene.gr_scene.drawBackground = types.MethodType(self.emtyDef, self)
        self.view.leftMouseButtonPress = types.MethodType(self.emtyDef, self)
        self.view.wheelEvent = types.MethodType(self.emtyDef, self)

    def emtyDef(self, *args):
        pass