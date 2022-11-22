from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge():
    def __init__(self, scene, start_sokcet, end_socket, edge_type=EDGE_TYPE_DIRECT) -> None:
        self.scene = scene
        self._start_socket = start_sokcet
        self._end_socket = end_socket
        self._edge_type = edge_type

        self._start_socket.edge = self
        if self._end_socket:
            self._end_socket.edge = self

        self.gr_edge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        self.scene.gr_scene.addItem(self.gr_edge)

    def removeFromSocket(self):
        if self._start_socket:
            self._start_socket.edge = None

        if self._end_socket:
            self._end_socket.edge = None

        self._start_socket = None
        self._end_socket = None

    def remove(self):
        self.removeFromSocket()
        self.scene.removeItem(self.gr_edge)
        self.gr_edge = None
        self.scene.removeEdge(self)

    def updatePositions(self):
        sourcePos = self._start_socket.getSocketPosition()
        sourcePos[0] += self._start_socket.node.gr_node.pos().x()
        sourcePos[1] += self._start_socket.node.gr_node.pos().y()
        self.gr_edge.setSource(*sourcePos)
        if self._end_socket:
            endPos = self._end_socket.getSocketPosition()
            endPos[0] += self._end_socket.node.gr_node.pos().x()
            endPos[1] += self._end_socket.node.gr_node.pos().y()
            self.gr_edge.setDestination(*endPos)

        self.gr_edge.update()