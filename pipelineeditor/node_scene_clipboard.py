from collections import OrderedDict

from pipelineeditor.node_edge import Edge
from pipelineeditor.node_node import Node
from pipelineeditor.graphics.node_graphics_edge import QDMGraphicsEdge


class SceneClipbaord():
    def __init__(self, scene) -> None:
        self.scene = scene

    def serializedSelected(self, delete=False):

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # Sort lists
        for item in self.scene.gr_scene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in item.node.inputs + item.node.outputs:
                    sel_sockets[socket.id] = socket
            elif isinstance(item, QDMGraphicsEdge):
                sel_edges.append(item.edge)

        # Remove edges that are not connected
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                pass
            else:
                edges_to_remove.append(edge)

        for edge in edges_to_remove:
            sel_edges.remove(edge)

        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())

        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edges_final)
        ])

        # delete in cut mode:
        if delete:
            self.scene.getView().deleteSelected()
            self.scene.history.store_history("Cut", True)

        return data

    def deserializeFromClipboard(self, data, adjust_pos=True):
        hashmap = {}

        # Calculate mouse pos
        view = self.scene.getView()
        mouse_scene_pos = view.last_mb_pos

        minx, maxx, miny, maxy = 10000000, -10000000, 10000000, -10000000

        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)

        maxx -= 180
        maxy += 100

        # Calculate selected object bbox and center
        # rel_bbox_center_x = (minx + maxx) / 2 - minx
        # rel_bbox_center_y = (miny + maxy) / 2 - miny

        mousex, mousey = mouse_scene_pos.x(), mouse_scene_pos.y()

        self.scene.setSilentSelectionEvents()
        self.scene.doDeselectItems()

        created_node = []
        # Create each node
        for node_data in data['nodes']:
            new_node = self.scene.get_node_class_from_data(node_data)(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)
            created_node.append(new_node)

            # readjust new_node position
            if adjust_pos:
                posx, posy = new_node.pos.x(), new_node.pos.y()
                newx, newy = mousex + posx - minx, mousey + posy - miny
                new_node.setPos(newx, newy)
            new_node.doSelect()

        # Create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)
                new_edge.doSelect()

        self.scene.setSilentSelectionEvents(False)

        # Store history
        self.scene.history.store_history('Paste', True)

        return created_node
