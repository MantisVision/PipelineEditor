from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsCutline(QGraphicsItem):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._line_points = []
        self._pen = QPen(Qt.white)
        self._pen.setWidth(2)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 1, 1)

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self._line_points)

        painter.drawPolyline(poly)