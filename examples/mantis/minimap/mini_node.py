from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MiniGRNode(QGraphicsItem):
    def __init__(self, node, parent=None) -> None:
        super().__init__(parent)
        self.node = node

        # init flags
        self._last_selected_state = False
        self.initSizes()
        self.initAssets()

        self.initUI()

    def initUI(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

    def initSizes(self):
        self.width = 160 // 8
        self.height = 74 // 8
        self.edge_roundness = 10 // 8

    def initAssets(self):
        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")

        self._pen_default = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))
        self._pen_default.setWidthF(1)
        self._pen_selected.setWidthF(1)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        # path_title = QPainterPath()
        # path_title.setFillRule(Qt.WindingFill)
        # path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        # path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        # path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        # painter.setPen(Qt.NoPen)
        # painter.setBrush(self._brush_title)
        # painter.drawPath(path_title.simplified())

        # contnet
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # # outline
        # path_outline = QPainterPath()
        # path_outline.addRoundedRect(-1, -1, self.width, self.height, self.edge_roundness, self.edge_roundness)
        # painter.setBrush(Qt.NoBrush)
        # if self.hovered:
        #     painter.setPen(self._pen_hovered)
        #     painter.drawPath(path_outline.simplified())
        #     painter.setPen(self._pen_default)
        #     painter.drawPath(path_outline.simplified())
        # else:
        #     painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        #     painter.drawPath(path_outline.simplified())


class MiniNode():
    GraphicNodeClass = MiniGRNode

    def __init__(self, scene, title="New Node") -> None:
        super().__init__()
        self._title = title
        self.scene = scene

        self.initInnerClasses()

        self.title = title

        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

    def initInnerClasses(self):
        self.gr_node = self.__class__.GraphicNodeClass(self)

    def isSelected(self):
        return self.gr_node.isSelected()

    def doSelect(self, new_state=True):
        self.gr_node.doSelect(new_state)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.gr_node.title = self._title

    @property
    def pos(self):
        return self.gr_node.pos()

    def setPos(self, x, y):
        self.gr_node.setPos(x, y)


    def onDoubleClicked(self, event):
        print("double click")
