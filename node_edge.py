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

        self.gr_edge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.scene.gr_scene.addItem(self.gr_edge)
