from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from collections import OrderedDict
from pipelineeditor.serialize.node_serializable import Serializable
from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket

LEFT_TOP     = 1
LEFT_CENTER  = 2
LEFT_BOTTOM  = 3
RIGHT_TOP    = 4
RIGHT_CENTER = 5
RIGHT_BOTTOM = 6


class Socket(Serializable):
    Socket_GR_Class = QDMGraphicsSocket

    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1, multi_edge=True, count_on_this_node_side=1, is_input=False) -> None:
        super().__init__()
        self.node = node
        self._position = position
        self._index = index
        self._socket_type = socket_type
        self.count_on_this_node_side = count_on_this_node_side
        self.multi_edge = multi_edge
        self.is_input = is_input
        self.is_output = not self.is_input

        self.gr_socket = self.__class__.Socket_GR_Class(self)
        self.setSocketPosition()

        self.edges = []

    def changeSocketType(self, new_socket_type):
        if self._socket_type != new_socket_type:
            self._socket_type = new_socket_type
            self.gr_socket.changeSocketType()

    def delete(self):
        self.gr_socket.setParentItem(None)
        self.node.scene.gr_scene.removeItem(self.gr_socket)
        del self.gr_socket

    def setSocketPosition(self):
        self.gr_socket.setPos(*self.node.getSocketsPosition(self._index, self._position, self.count_on_this_node_side))

    def has_edge(self):
        return len(self.edges) > 0

    def is_connected(self, edge):
        return edge in self.edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("Edge not found in remove")

    def remove_all_edges(self, silent=False):
        while self.edges:
            edge = self.edges.pop(0)
            if silent:
                edge.remove(silent_for_socket=self)
            else:
                edge.remove()

    def getSocketPosition(self):
        return self.node.getSocketsPosition(self._index, self._position, self.count_on_this_node_side)

    def determineMultiEdges(self, data):
        if 'multi_edges' in data:
            return data['multi_edges']
        else:
            return data['position'] in (RIGHT_TOP, RIGHT_TOP)

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self._index),
            ('multi_edge', self.multi_edge),
            ('position', self._position),
            ('socket_type', self._socket_type)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data['id']
        self.multi_edge = self.determineMultiEdges(data)
        hashmap[data['id']] = self
        return True