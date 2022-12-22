from pipelineeditor.graphics.node_graphics_node import QDMGraphicsNode
from pipelineeditor.node_content_widget import QDMNodeContentWidget

from pipelineeditor.serialize.node_serializable import Serializable
from pipelineeditor.node_socket import *
from pipelineeditor.utils import dump_exception

class Node(Serializable):
    def __init__(self, scene, title="New Node", inputs=[], outputs=[]) -> None:
        super().__init__()
        self._title = title
        self.scene = scene
        self._socket_gap = 20
        self.content = QDMNodeContentWidget(self)
        self.gr_node = QDMGraphicsNode(self)
        self.title = title
        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

        # self.grNode.title = "ASDASDAD"

        self.inputs = []
        self.outputs = []

        counter = 0
        for i in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=i, multi_edge=False)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for o in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=i, multi_edge=True)
            self.outputs.append(socket)
            counter += 1

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            for edge in socket.edges:
                edge.updatePositions()

    def getSocketsPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.gr_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.gr_node.height - self.gr_node.edge_size - self.gr_node._padding - index * self._socket_gap
        else:
            y = self.gr_node.title_height + self.gr_node._padding + self.gr_node.edge_size + index * self._socket_gap

        return [x, y]

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.gr_node.title = self._title

    @property
    def pos(self):
        return self.gr_node.pos()

    def setPos(self, x, y):
        self.gr_node.setPos(x, y)

    def remove(self):
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.remove()
        self.scene.gr_scene.removeItem(self.gr_node)
        self.gr_node = None
        self.scene.remove_node(self)

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

    def deserialize(self, data, hashmap={}, restore_id=True):
        try:
            if restore_id:
                self.id = data['id']
            hashmap[data['id']] = self

            self.setPos(data['pos_x'], data['pos_y'])
            self.title = data['title']

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 1000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 1000)

            self.inputs = []
            for socket_data in data['inputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.outputs.append(new_socket)
        except Exception as e:
            dump_exception(e)

        return True