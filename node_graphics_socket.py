from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None, socket_type=1) -> None:
        super().__init__(parent)

        self._radius = 6
        self._socket_type = socket_type
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF528220"),
            QColor("#FF0056a6"),
            QColor("#FF886db1"),
            QColor("#FFb54747"),
            QColor("#FFdbe220")
        ]
        self._outline_width = 1
        self._color_background = self._colors[self._socket_type]
        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidth(self._outline_width)
        self._brush = QBrush(self._color_background)

    def boundingRect(self):
        return QRectF(
            -self._radius - self._outline_width,
            -self._radius - self._outline_width,
            2 * (self._radius + self._outline_width),
            2 * (self._radius + self._outline_width),
        )

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

        painter.drawEllipse(-self._radius, -self._radius, 2 * self._radius, 2 * self._radius)