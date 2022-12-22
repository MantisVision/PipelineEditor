import json
from collections import OrderedDict
from pipelineeditor.node_node import Node
from pipelineeditor.node_edge import Edge
from pipelineeditor.utils import dump_exception
from pipelineeditor.graphics.node_graphics_scene import QDMGraphicsScene
from pipelineeditor.serialize.node_serializable import Serializable
from pipelineeditor.node_scene_history import SceneHistory
from pipelineeditor.node_scene_clipboard import SceneClipbaord


class InvalidFile(Exception):
    pass


class Scene(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000
        self.history = SceneHistory(self)
        self.clipboard = SceneClipbaord(self)
        self._has_been_modified = False
        self._has_been_modified_listeners = []
        self.initUI()

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, val):
        if not self.has_been_modified and val:
            self._has_been_modified = val

            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = val

    def add_has_been_modified_listener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        # Create graphics scene
        self.gr_scene = QDMGraphicsScene(self)
        self.gr_scene.setGrScene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()
        self.has_been_modified = False

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.serialize(), indent=4))
            print(f"Saving to {filename} was successful")
            self.has_been_modified = False

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.loads(f.read())
                self.deserialize(data)
                self.has_been_modified = False
        except json.JSONDecodeError:
            raise InvalidFile(f"{filename} is not a valid JSON file")
        except Exception as e:
            dump_exception(e)

    def serialize(self):
        nodes = [node.serialize() for node in self.nodes]
        edges = [edge.serialize() for edge in self.edges]
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}

        if restore_id:
            self.id = data['id']

        # Load nodes
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)

        # Load Edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True