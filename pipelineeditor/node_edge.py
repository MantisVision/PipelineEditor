from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from collections import OrderedDict
from pipelineeditor.serialize.node_serializable import Serializable
from pipelineeditor.graphics.node_graphics_edge import *
from pipelineeditor.utils import dump_exception

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_TYPE_SQUARE = 3
EDGE_TYPE_DEFAULT = EDGE_TYPE_BEZIER


class Edge(Serializable):
    def __init__(self, scene, start_sokcet=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT) -> None:
        super().__init__()
        self.scene = scene
        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_sokcet
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.add_edge(self)

    def doSelect(self, new_state=True):
        self.gr_edge.doSelect(new_state)

    @property
    def start_socket(self):
        return self._start_socket

    @start_socket.setter
    def start_socket(self, val):
        if self._start_socket:
            self._start_socket.remove_edge(self)

        self._start_socket = val
        if self.start_socket:
            self.start_socket.add_edge(self)

    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, val):
        if self._end_socket:
            self._end_socket.remove_edge(self)

        self._end_socket = val
        if self.end_socket:
            self.end_socket.add_edge(self)

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
        elif self.edge_type == EDGE_TYPE_SQUARE:
            self.gr_edge = GraphicsEdgePathSquare(self)
        else:
            self.gr_edge = QDMGraphicsEdgeBezier(self)

        self.scene.gr_scene.addItem(self.gr_edge)

        if self.start_socket:
            self.updatePositions()

    def getOtherSocket(self, known_socket):
        return self.start_socket if known_socket == self.end_socket else self.end_socket

    def removeFromSocket(self):
        self.start_socket = None
        self.end_socket = None

    def remove(self, silent_for_socket=None, silent=False):
        old_sockets = [self.start_socket, self.end_socket]

        self.removeFromSocket()
        self.scene.gr_scene.removeItem(self.gr_edge)
        self.gr_edge = None

        try:
            self.scene.remove_edge(self)
        except ValueError:
            pass

        # notify nodes from old sockets
        try:
            for socket in old_sockets:
                if socket and socket.node:
                    if silent:
                        continue
                    if silent_for_socket and socket == silent_for_socket:
                        continue
                    socket.node.onEdgeConnectionChanged(self)
                    # TODO: check this uncomment this line
                    # if socket.is_input:
                    socket.node.onInputChanged(socket)
        except Exception as e:
            dump_exception(e)

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
            ('start', self.start_socket.id if self.start_socket else None),
            ('end', self.end_socket.id if self.end_socket else None)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data['id']

        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
