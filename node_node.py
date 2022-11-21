from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *


class Node():
    def __init__(self, scene, title="New Node", inputs=[], outputs=[]) -> None:
        self.scene = scene
        self.title = title
        self._socket_gap = 20
        self.content = QDMNodeContentWidget()
        self.gr_node = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.gr_scene.addItem(self.gr_node)

        # self.grNode.title = "ASDASDAD"

        self.inputs = []
        self.outputs = []

        counter = 0
        for i in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for o in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTOM)
            self.outputs.append(socket)
            counter += 1

    def getSocketsPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.gr_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = (self.gr_node.height - self.gr_node._padding - self.gr_node.edge_size) - (index * self._socket_gap)
        else:
            y = (self.gr_node.title_height + self.gr_node._padding + self.gr_node.edge_size) + (index * self._socket_gap)

        return x, y