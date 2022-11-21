from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._width = 2

        self._pen = QPen(self._color)
        self._pen.setWidth(self._width)

        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidth(self._width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None) -> None:
        self.updatePath()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        raise NotImplementedError("This method must be overriden by the child class")


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(QPointF(self.posDestination[0], self.posDestination[1]))
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination

        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]:
            dist = -dist

        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(
            s[0] + dist,
            s[1],
            d[0] - dist,
            d[1],
            d[0],
            d[1]
        )

        self.setPath(path)