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

        self.initInnerClasses()
        self.initSettings()

        self.title = title

        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

        self.inputs = []
        self.outputs = []
        self.initSockets(inputs, outputs)

        self._is_dirty = False
        self._is_invalid = False

    def initInnerClasses(self):
        self.content = QDMNodeContentWidget(self)
        self.gr_node = QDMGraphicsNode(self)

    def initSettings(self):
        self._socket_gap = 20
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edge = False
        self.output_multi_edge = True

    def initSockets(self, inputs, outputs, reset=True):
        """ Create sockets for inputs and outputs """

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                for socket in (self.inputs + self.outputs):
                    self.scene.gr_scene.removeItem(socket.gr_socket)
                self.inputs = []
                self.outputs = []

        # Create new sockets
        counter = 0
        for i in inputs:
            socket = Socket(
                node=self,
                index=counter,
                position=self.input_socket_position,
                socket_type=i,
                multi_edge=self.input_multi_edge,
                count_on_this_node_side=len(inputs),
                is_input=True,
            )
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for o in outputs:
            socket = Socket(
                node=self,
                index=counter,
                position=self.output_socket_position,
                socket_type=o,
                multi_edge=self.output_multi_edge,
                count_on_this_node_side=len(outputs),
                is_input=False,
            )
            self.outputs.append(socket)
            counter += 1

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            for edge in socket.edges:
                edge.updatePositions()

    def getSocketsPosition(self, index, position, num_out_off=1):
        x = 0 if position in (LEFT_TOP, LEFT_CENTER, LEFT_BOTTOM) else self.gr_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.gr_node.height - self.gr_node.edge_roundness - self.gr_node._title_vertical_padding - index * self._socket_gap
        elif position in (LEFT_CENTER, RIGHT_CENTER):
            num_socket = num_out_off
            node_height = self.gr_node.height
            top_offset = self.gr_node.title_height + 2 * self.gr_node._title_vertical_padding + self.gr_node.edge_padding
            available_heigt = node_height - top_offset
            total_height_of_all_socket = num_socket * self._socket_gap
            new_top = available_heigt - total_height_of_all_socket
            # y = top_offset + index * self._socket_gap + new_top / 2

            y = top_offset + (available_heigt / 2) + (index - 0.5) * self._socket_gap
            if num_socket > 1:
                y -= (self._socket_gap * (num_socket - 1)) / 2
        elif position in (LEFT_TOP, RIGHT_TOP):
            y = self.gr_node.title_height + self.gr_node._title_vertical_padding + self.gr_node.edge_roundness + index * self._socket_gap
        else:
            # this condition never happend
            y = 0

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

    def setContentTitle(self, title):
        self.content.setTitle(title)

    def onDoubleClicked(self, event):
        """Event handling double click on Graphics Node in `Scene`"""
        print("double click")

    def remove(self):
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.remove()
        self.scene.gr_scene.removeItem(self.gr_node)
        self.gr_node = None
        self.scene.remove_node(self)

    # Node evaluation functions
    def isDirty(self):
        return self._is_dirty

    def markDirty(self, val=True):
        self._is_dirty = val
        if self._is_dirty:
            self.onMarkedDirty()

    def isInvalid(self):
        return self._is_invalid

    def markInvalid(self, val=True):
        self._is_invalid = val
        if self._is_invalid:
            self.onMarkedDirty()

    def onMarkedDirty(self):
        pass

    def onMarkedInvalid(self):
        pass

    def eval(self):
        self.markDirty(False)
        self.markInvalid(False)
        return 0

    def evalChildren(self):
        for node in self.getChildrenNode():
            node.eval()

    def markChildrenDirty(self, val=True):
        for child_node in self.getChildrenNode():
            child_node.markDirty(val)
            # added recursion for marking the whole descendatns tree
            child_node.markChildrenDirty()

    def markDescendantsDirty(self, val=True):
        for child_node in self.getChildrenNode():
            child_node.markDirty(val)
            child_node.markChildrenDirty(val)

    def markChildrenInvalid(self, val=True):
        for child_node in self.getChildrenNode():
            child_node.markInvalid(val)
            # added recursion for marking the whole descendatns tree
            child_node.markChildrenInvalid()

    def markDescendantsInvalid(self, val=True):
        for child_node in self.getChildrenNode():
            child_node.markInvalid(val)
            child_node.markChildrenInvalid(val)

    def getChildrenNode(self):
        if self.outputs == []:
            return []
        child_nodes = []
        for i in range(len(self.outputs)):
            for edge in self.outputs[i].edges:
                child = edge.getOtherSocket(self.outputs[i]).node
                child_nodes.append(child)

        return child_nodes

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
            num_inputs = len(data['inputs'])
            num_outputs = len(data['outputs'])

            self.inputs = []
            for socket_data in data['inputs']:
                new_socket = Socket(
                    node=self,
                    index=socket_data['index'],
                    position=socket_data['position'],
                    socket_type=socket_data['socket_type'],
                    count_on_this_node_side=num_inputs,
                    is_input=True
                )
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(
                    node=self,
                    index=socket_data['index'],
                    position=socket_data['position'],
                    socket_type=socket_data['socket_type'],
                    count_on_this_node_side=num_outputs,
                    is_input=False
                )
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.outputs.append(new_socket)
        except Exception as e:
            dump_exception(e)

        # Deserialize node content
        res = self.content.deserialize(data['content'], hashmap)

        return True & res