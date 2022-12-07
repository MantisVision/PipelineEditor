from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from serialize.node_serializable import Serializable
from graphics.node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge(Serializable):
    def __init__(self, scene, start_sokcet=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT) -> None:
        super().__init__()
        self.scene = scene
        self.start_socket = start_sokcet
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)

    @property
    def start_socket(self):
        return self._start_socket

    @start_socket.setter
    def start_socket(self, val):
        self._start_socket = val
        if self.start_socket:
            self.start_socket.edge = self

    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, val):
        self._end_socket = val
        if self.end_socket:
            self.end_socket.edge = self

    @property
    def edge_type(self):
        return self._edge_type

    @edge_type.setter
    def edge_type(self, val):
        if hasattr(self, 'gr_edge') and self.gr_edge:
            self.scene.gr_scene.removeItem(self.gr_edge)

        self._edge_type = val
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.gr_edge = QDMGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.gr_edge = QDMGraphicsEdgeBezier(self)
        else:
            self.gr_edge = QDMGraphicsEdgeBezier(self)

        self.scene.gr_scene.addItem(self.gr_edge)

        if self.start_socket:
            self.updatePositions()

    def removeFromSocket(self):
        if self.start_socket:
            self.start_socket.edge = None

        if self.end_socket:
            self.end_socket.edge = None

        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.removeFromSocket()
        self.scene.gr_scene.removeItem(self.gr_edge)
        self.gr_edge = None

        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass

    def updatePositions(self):
        sourcePos = self.start_socket.getSocketPosition()
        sourcePos[0] += self.start_socket.node.gr_node.pos().x()
        sourcePos[1] += self.start_socket.node.gr_node.pos().y()
        self.gr_edge.setSource(*sourcePos)
        if self.end_socket:
            endPos = self.end_socket.getSocketPosition()
            endPos[0] += self.end_socket.node.gr_node.pos().x()
            endPos[1] += self.end_socket.node.gr_node.pos().y()
            self.gr_edge.setDestination(*endPos)
        else:
            self.gr_edge.setDestination(*sourcePos)
        self.gr_edge.update()

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id)
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
        # hashmap[data['id']] = self
