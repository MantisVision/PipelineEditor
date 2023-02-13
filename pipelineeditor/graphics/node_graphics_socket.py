from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

SOCKET_COLORS = [
    QColor("#FFFF7700"),
    QColor("#FF528220"),
    QColor("#FF0056a6"),
    QColor("#FF886db1"),
    QColor("#FFb54747"),
    QColor("#FFdbe220")
]


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1) -> None:
        self.socket = socket
        super().__init__(socket.node.gr_node)

        self._radius = 6
        self._socket_type = socket_type
        self._outline_width = 1
        self._color_background = self.getSocketColor[self._socket_type]
        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidth(self._outline_width)
        self._brush = QBrush(self._color_background)

    def getSocketColor(self, key):
        if type(key) == int:
            return SOCKET_COLORS[key]
        elif type(key) == str:
            return QColor(key)
        return Qt.transparent

    def mousePressEvent(self, QGraphicsSceneMouseEvent) -> None:
        print("Socket is clicked")

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