from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_socket import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1) -> None:
        self.node = node
        self._position = position
        self._index = index
        self._socket_type = socket_type
        self.gr_socket = QDMGraphicsSocket(self.node.gr_node, self._socket_type)

        self.gr_socket.setPos(*self.node.getSocketsPosition(self._index, self._position))

        self.edge = None

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def getSocketPosition(self):
        return self.node.getSocketsPosition(self._index, self._position)

    def hasEdge(self):
        return self.edge is not None