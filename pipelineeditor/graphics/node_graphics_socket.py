from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

SOCKET_COLORS = [
    QColor("#FFFF7700"),
    QColor("#FF52e220"),
    QColor("#FF0056a6"),
    QColor("#FFa86db1"),
    QColor("#FFb54747"),
    QColor("#FFdbe220"),
    QColor("#FF888888"),
]


class QDMGraphicsSocket(QGraphicsItem):

    def __init__(self, socket):
        super().__init__(socket.node.gr_node)

        self.socket = socket

        self.radius = 6.0
        self.outline_width = 1.0
        self.initAssets()

    @property
    def socket_type(self):
        return self.socket._socket_type

    def getSocketColor(self, key):
        if type(key) == int:
            return SOCKET_COLORS[key]
        elif type(key) == str:
            return QColor(key)
        return Qt.transparent

    def changeSocketType(self):
        """Change the Socket Type"""
        self._color_background = self.getSocketColor(self.socket_type)
        self._brush = QBrush(self._color_background)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def initAssets(self):

        # determine socket color
        self._color_background = self.getSocketColor(self.socket_type)
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )