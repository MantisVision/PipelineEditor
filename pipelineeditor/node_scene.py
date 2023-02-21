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
        self.gr_scene = None
        self.scene_width = 6400
        self.scene_height = 6400
        self.history = SceneHistory(self)
        self.clipboard = SceneClipbaord(self)

        # init listeners
        self._has_been_modified = False
        self._silent_selection_events = False
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []
        self._last_selected_items = None

        # here we can store callback for retrieving the class for Nodes
        self.node_class_selector = None

        self.initUI()

        self.gr_scene.itemSelected.connect(self.onItemSelected)
        self.gr_scene.itemsDeselected.connect(self.onItemsDeselected)

    def initUI(self):
        self.gr_scene = QDMGraphicsScene(self)
        self.gr_scene.setGrScene(self.scene_width, self.scene_height)

    def getNodeByID(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def setSilentSelectionEvents(self, value=True):
        self._silent_selection_events = value

    def onItemSelected(self, silent=False):
        if self._silent_selection_events:
            return

        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items

            if not silent:
                for callback in self._item_selected_listeners:
                    callback()
                self.history.store_history("Selection Changed")

    def onItemsDeselected(self, silent=False):
        current_selected_items = self.getSelectedItems()
        if current_selected_items == self._last_selected_items:
            return
        
        self.resetLastSelectedStates()
        if self._last_selected_items == []:
            self._last_selected_items = []

            if not silent:
                self.history.store_history("Deselction items")
                for callback in self._items_deselected_listeners:
                    callback()

    def doDeselectItems(self, silent=False):
        for item in self.getSelectedItems():
            item.setSelected(False)
        if not silent:
            self.onItemsDeselected()

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.gr_scene.selectedItems()

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, val):
        if not self.has_been_modified and val:
            # set it now because we will read it soon
            self._has_been_modified = val

            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = val

    def add_has_been_modified_listener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def add_item_selected_listener(self, callback):
        self._item_selected_listeners.append(callback)

    def add_items_deselected_listener(self, callback):
        self._items_deselected_listeners.append(callback)

    def add_drag_enter_listener(self, callback):
        self.getView().addDragEnterListener(callback)

    def add_drop_listener(self, callback):
        self.getView().addDropListener(callback)

    def add_item_doubleclick_listener(self, callback):
        self.getView().addDoubleClickListener(callback)

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.gr_node._last_selected_state = False

        for edge in self.edges:
            edge.gr_edge._last_selected_state = False

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

    def getEdgeClass(self):
        """Return the class representing Edge. Override me if needed"""
        return Edge

    def set_node_class_selector(self, class_selectinf_func):
        self.node_class_selector = class_selectinf_func

    def get_node_class_from_data(self, data):
        return Node if not self.node_class_selector else self.node_class_selector(data)

    def getView(self):
        return self.gr_scene.views()[0]

    def getItemAt(self, pos):
        return self.getView().itemAt(pos)

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
        hashmap = {}

        if restore_id:
            self.id = data['id']

        # -- deserialize NODES
        # Instead of recreating all the nodes, reuse existing ones...
        # get list of all current nodes:
        all_nodes = self.nodes.copy()

        # go through deserialized nodes:
        for node_data in data['nodes']:
            # can we find this node in the scene?
            found = False
            for node in all_nodes:
                if node.id == node_data['id']:
                    found = node
                    break

            if not found:
                new_node = self.get_node_class_from_data(node_data)(self)
                new_node.deserialize(node_data, hashmap, restore_id)
                new_node.onDeserialized(node_data)
                # print("New node for", node_data['title'])
            else:
                found.deserialize(node_data, hashmap, restore_id)
                found.onDeserialized(node_data)
                all_nodes.remove(found)
                # print("Reused", node_data['title'])

        # remove nodes which are left in the scene and were NOT in the serialized data!
        # that means they were not in the graph before...
        while all_nodes != []:
            node = all_nodes.pop()
            node.remove()

        # -- deserialize EDGES
        # Instead of recreating all the edges, reuse existing ones...
        # get list of all current edges:
        all_edges = self.edges.copy()

        # go through deserialized edges:
        for edge_data in data['edges']:
            # can we find this node in the scene?
            found = False
            for edge in all_edges:
                if edge.id == edge_data['id']:
                    found = edge
                    break

            if not found:
                new_edge = Edge(self).deserialize(edge_data, hashmap, restore_id)
                # print("New edge for", edge_data)
            else:
                found.deserialize(edge_data, hashmap, restore_id)
                all_edges.remove(found)

        # remove nodes which are left in the scene and were NOT in the serialized data!
        # that means they were not in the graph before...
        while all_edges != []:
            edge = all_edges.pop()
            edge.remove()

        return True
