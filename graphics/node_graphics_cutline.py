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
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        poly = QPolygonF(self._line_points)

        if len(self._line_points) > 1:
            path = QPainterPath(self._line_points[0])
            for pt in self._line_points[1:]:
                path.lineTo(pt)
        else:
            path = QPainterPath(QPointF(0, 0))
            path.lineTo(QPointF(1, 1))

        return path

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self._line_points)

        painter.drawPolyline(poly)