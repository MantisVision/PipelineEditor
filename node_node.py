from graphics.node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget

from serialize.node_serializable import Serializable
from node_socket import *


class Node(Serializable):
    def __init__(self, scene, title="New Node", inputs=[], outputs=[]) -> None:
        super().__init__()
        self.scene = scene
        self.title = title
        self._socket_gap = 20
        self.content = QDMNodeContentWidget(self)
        self.gr_node = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.gr_scene.addItem(self.gr_node)

        # self.grNode.title = "ASDASDAD"

        self.inputs = []
        self.outputs = []

        counter = 0
        for i in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=i)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for o in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=i)
            self.outputs.append(socket)
            counter += 1

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def getSocketsPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.gr_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.gr_node.height - self.gr_node.edge_size - self.gr_node._padding - index * self._socket_gap
        else:
            y = self.gr_node.title_height + self.gr_node._padding + self.gr_node.edge_size + index * self._socket_gap

        return [x, y]

    @property
    def pos(self):
        return self.gr_node.pos()

    def setPos(self, x, y):
        self.gr_node.setPos(x, y)

    def remove(self):
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                socket.edge.remove()
        self.scene.gr_scene.removeItem(self.gr_node)
        self.gr_node = None
        self.scene.removeNode(self)

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.gr_node.scenePos().x()),
            ('pos_y', self.gr_node.scenePos().y()),
            ('inputs', [socket.serialize() for socket in self.inputs]),
            ('outputs', [socket.serialize() for socket in self.outputs]),
            ('content', self.content.serialize())
        ])

    def deserialize(self, data, hashmap={}):
        print(data)